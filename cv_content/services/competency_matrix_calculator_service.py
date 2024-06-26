import json
import math
from collections import defaultdict
from typing import List

import pandas as pd
from loguru import logger

from utils.llm_connector import LlmConnector
from cv_content.schemas import JobPosition, Competency, Project


class CompetencyMatrixCalculatorService:

    def __init__(self, llm_connector=LlmConnector()):
        self.llm_connector = llm_connector

    def build(self, jobs: List[JobPosition], projects: List[Project], background_competencies: List[Competency] = None):
        background_competencies = background_competencies or []
        job_competencies = self.generate_competencies_from_job_positions(jobs)
        project_competencies = self.generate_competencies_from_generic_projects(projects)
        competencies = self.merge_competencies(background_competencies, job_competencies, project_competencies)
        return competencies

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
        competencies_matching = self.llm_connector.try_load_as_json_list(response)
        return competencies_matching

    def generate_competencies_from_job_positions(self, job_positions: List[JobPosition]) -> List[Competency]:
        competencies = defaultdict(lambda: {'last_used': 0, 'years_of_experience': 0})

        for job in job_positions:
            years_of_exp = (job.end_date - job.start_date).days / 365.25

            for comp_name in job.competencies:
                competencies[comp_name]['last_used'] = max(job.end_date.year, competencies[comp_name]['last_used'])
                competencies[comp_name]['years_of_experience'] += years_of_exp

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

    def generate_competencies_from_generic_projects(self, projects: List[Project]) -> List[Competency]:
        competencies: List[Competency] = []
        for project in projects:
            for competency_name in project.competencies:
                competency = next(filter(lambda x: Competency.strip_competency_name_for_comparison(
                    x.name) == Competency.strip_competency_name_for_comparison(competency_name), competencies), None)

                if competency:
                    competency.years_of_experience += project.effort_in_years
                    competency.last_used = max(competency.last_used, project.last_updated.year)
                else:
                    competencies.append(Competency(
                        name=competency_name,
                        level=1,
                        last_used=project.last_updated.year,
                        years_of_experience=project.effort_in_years
                    ))
        logger.debug(f"project competencies: {[comp.name for comp in competencies]}")
        return competencies

    def merge_competencies(self, background_competencies: List[Competency], job_competencies: List[Competency],
                           project_competencies: List[Competency]) -> List[Competency]:
        if len(job_competencies) == 0 and len(project_competencies) == 0:
            logger.info("No competencies found in jobs or projects")
            return background_competencies

        # make a group by name and sum on experience, max on last used, and
        background_competencies_pd = self.pydantic_list_to_pandas(background_competencies, Competency)
        job_competencies_pd = self.pydantic_list_to_pandas(job_competencies, Competency)
        project_competencies_pd = self.pydantic_list_to_pandas(project_competencies, Competency)

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
        self.df_add_stripped_name_for_comparison(job_project_competencies_pd)
        competencies_merged = job_project_competencies_pd.groupby('name_compare').agg({
            "name": "first",
            "years_of_experience": 'max',
            'last_used': 'max',
            "level": "max",
            "category": "first",
            "attractiveness": "max",
        })
        return competencies_merged

    def df_add_stripped_name_for_comparison(self, job_project_competencies_pd: pd.DataFrame, column_name='name'):
        job_project_competencies_pd[column_name + "_compare"] = job_project_competencies_pd.apply(
            lambda x: Competency.strip_competency_name_for_comparison(x[column_name]), axis=1)

    def sum_years_of_experience_on_jobs_and_projects(self, job_competencies_pd, project_competencies_pd):
        job_project_competencies_pd = pd.concat([job_competencies_pd, project_competencies_pd], ignore_index=True)
        self.df_add_stripped_name_for_comparison(job_project_competencies_pd)
        job_project_competencies_grouped = job_project_competencies_pd.groupby('name_compare').agg({
            "name": "first",
            "years_of_experience": 'sum',
            'last_used': 'max',
            "level": "max",
            "category": "first",
        })
        return job_project_competencies_grouped

    def pydantic_list_to_pandas(self, list_of_objects, model):
        column_names = model.__fields__.keys()
        logger.debug(f"column names: {column_names}")
        return pd.DataFrame([c.dict() for c in list_of_objects], columns=column_names)
