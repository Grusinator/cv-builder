import json
import math
from collections import defaultdict
from typing import List

import pandas as pd
from loguru import logger

from cv_compiler.llm_connector import ChatGPTInterface
from cv_compiler.models import Competency, JobPosition, JobApplication, GithubProject


class CompetencyMatrixCalculator:

    def __init__(self, llm_connector: ChatGPTInterface):
        self.llm_connector = llm_connector

    def build(self, jobs: List[JobPosition], projects: List[GithubProject], job_application: JobApplication,
              background_competencies: List[Competency]):
        job_competencies = self.generate_competencies_from_job_positions(jobs)
        project_competencies = self.generate_competencies_from_projects(projects)
        competencies = self.merge_competencies(background_competencies, job_competencies, project_competencies)
        relevant_competencies = self.find_most_relevant_competencies_to_job_add(job_application.job_description,
                                                                                competencies)
        return relevant_competencies

    def find_most_relevant_competencies_to_job_add(self, job_description: str, competencies, n=15) -> List[
        Competency]:
        competencies_ordered = self.filter_matching_competencies_from_job_application(competencies, job_description)

        if len(competencies_ordered) > n:
            competencies_ordered = competencies_ordered[:n]
        attractive_competencies = [comp for comp in competencies if comp.name in competencies_ordered]
        logger.debug(f"Most attractive competencies: {attractive_competencies}")
        return attractive_competencies

    def filter_matching_competencies_from_job_application(self, competencies, job_description):
        competency_names = [comp.name for comp in competencies]
        question = f"""
        sort these competencies by attractiveness for this job, focus on the title and tell me what skills 
        are relevant for this job. also look at the skills mentioned in the job description, 
        and if there are similar skill, then put them in the top. 

        Job decription:
        {job_description}
        --------------------
        Competencies:        
        {json.dumps(competency_names)}
        --------------------
        it should be formattet as json as a list of strings, and the response should only include the json list, like this:

        ["Python", "Data engineering", "Machine learning"]

        """
        response = self.llm_connector.ask_question(question)
        logger.debug(f"Response: {response}")
        competencies_ordered = self.llm_connector.try_load_as_json_list(response)
        return competencies_ordered

    def extract_competencies_from_job_description(self, job_description: str, competencies: List[Competency]) -> List[
        str]:
        question = f"""What are the competencies required for the job: 
        \n\n {job_description} \n\n 
        The competencies should be formatted as a single list of strings, such as ["python", "javascript"]
        if any of the competencies mentioned are semantically the same as the competencies in the list below, then use
        the values from the list below. 
        \n\n{",".join([comp.name for comp in competencies])}\n\n"""

        response = self.llm_connector.ask_question(question)
        competencies = self.llm_connector.try_load_as_json_list(response)
        return competencies

    def generate_competencies_from_job_positions(self, job_positions: List[JobPosition]) -> List[Competency]:
        competencies = defaultdict(lambda: {'last_used': 0, 'years_of_experience': 0})

        for job in job_positions:
            years_of_exp = (job.end_date - job.start_date).days / 365.25

            for tech in job.technologies:
                competencies[tech]['last_used'] = max(job.end_date.year, competencies[tech]['last_used'])
                competencies[tech]['years_of_experience'] += years_of_exp

        competencies = [
            Competency(
                name=tech,
                level=1,
                last_used=data['last_used'],
                years_of_experience=math.ceil(data['years_of_experience'])
            )
            for tech, data in competencies.items()
        ]
        logger.debug(f"job competencies: {[comp.name for comp in competencies]}")
        return competencies

    def strip_competency_name_for_comparison(self, competency_name: str) -> str:
        return competency_name.lower().replace(" ", "").replace("-", "")

    def generate_competencies_from_projects(self, projects: List[GithubProject]) -> List[Competency]:
        competencies: List[Competency] = []
        for project in projects:
            for competency_name in project.technologies + project.languages:
                competency = next(filter(lambda x: x.name == competency_name, competencies), None)
                year_of_experience = max(0.25, project.number_of_weeks_with_commits / 47)
                if competency:
                    competency.years_of_experience += year_of_experience
                    competency.last_used = max(competency.last_used, project.last_commit.year)
                else:
                    competencies.append(Competency(
                        name=competency_name,
                        level=1,
                        last_used=project.last_commit.year,
                        years_of_experience=year_of_experience
                    ))
        logger.debug(f"project competencies: {[comp.name for comp in competencies]}")
        return competencies

    def merge_competencies(self, background_competencies: List[Competency], job_competencies: List[Competency],
                           project_competencies: List[Competency]) -> List[Competency]:
        # make a group by name and sum on experience, max on last used, and
        background_competencies_pd = self.pydantic_list_to_pandas(background_competencies)
        job_competencies_pd = self.pydantic_list_to_pandas(job_competencies)
        project_competencies_pd = self.pydantic_list_to_pandas(project_competencies)

        job_project_competencies_grouped = self.sum_years_of_experience_on_jobs_and_projects(job_competencies_pd,
                                                                                             project_competencies_pd)

        competencies_merged_pd = self.aggregate_max_with_background_competencies(background_competencies_pd,
                                                                                 job_project_competencies_grouped)
        competencies = self.convert_pandas_to_pydantic(competencies_merged_pd)
        logger.debug(f"merged competencies: {[comp.name for comp in competencies]}")
        return competencies

    def convert_pandas_to_pydantic(self, dataframe: pd.DataFrame, model=Competency):
        dataframe = dataframe.fillna({'attractiveness': 3}).astype({"attractiveness": int})
        competencies = [model.model_validate(row) for row in dataframe.to_dict(orient="records")]
        return competencies

    def aggregate_max_with_background_competencies(self, background_competencies_pd, job_project_competencies_grouped):
        job_project_competencies_pd = pd.concat([background_competencies_pd, job_project_competencies_grouped],
                                                ignore_index=True)
        competencies_merged = job_project_competencies_pd.groupby('name').agg({
            "years_of_experience": 'max',
            'last_used': 'max',
            "level": "max",
            "category": "first",
            "attractiveness": "max",
        })
        return competencies_merged.reset_index()

    def sum_years_of_experience_on_jobs_and_projects(self, job_competencies_pd, project_competencies_pd):
        job_project_competencies_pd = pd.concat([job_competencies_pd, project_competencies_pd], ignore_index=True)
        job_project_competencies_grouped = job_project_competencies_pd.groupby('name').agg({
            "years_of_experience": 'sum',
            'last_used': 'max',
            "level": "max",
            "category": "first",
        })
        return job_project_competencies_grouped.reset_index()

    def pydantic_list_to_pandas(self, list_of_objects):
        return pd.DataFrame([c.dict() for c in list_of_objects])
