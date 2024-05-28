import json
import math
from typing import List
from collections import defaultdict

from dotenv import load_dotenv

from cv_compiler.file_handler import FileHandler
from cv_compiler.github_projects import GitHubProjectFetcher
from cv_compiler.llm_connector import ChatGPTInterface
from cv_compiler.models import JobPosition, Competency

load_dotenv()

from loguru import logger


class CVContentBuilder:

    def __init__(self):
        self.file_handler = FileHandler()
        self.github_fetcher = GitHubProjectFetcher()
        self.chatgpt_interface = ChatGPTInterface()
        self._projects = []

    def build_all(self):
        self.build_job_positions()
        relevant_competencies = self.get_competencies_from_job_description_subset_of_job_positions()
        self.build_competency_matrix(relevant_competencies)
        self.build_projects(relevant_competencies)
        self.build_summary()

    def get_projects(self):
        if len(self._projects) == 0:
            self._projects = self.github_fetcher.fetch_all()
        return self._projects

    def build_competency_matrix(self, competencies):
        self.file_handler.write_competency_matrix_generated(competencies)

    def get_competencies_from_job_description_subset_of_job_positions(self):
        jobs = self.file_handler.get_background_job_positions()
        competencies = self.generate_competencies_from_job_positions(jobs)
        logger.debug(f"Competencies from job positions: {competencies}")
        job_add_description = self.file_handler.read_job_description()
        job_add_competencies = self.extract_competencies_from_job_description(job_add_description, competencies)
        logger.debug(f"Job competencies: {job_add_competencies}")
        filtered_competencies = self.filter_union_of_competencies(competencies, job_add_competencies)
        logger.debug(f"Filtered competencies: {filtered_competencies}")
        return filtered_competencies

    def filter_union_of_competencies(self, competencies: List[Competency], job_add_competencies: List[str]) -> List[
        Competency]:
        job_add_competencies_stripped = [self.strip_competency_name_for_comparison(comp) for comp in
                                         job_add_competencies]
        filtered_competencies = [comp for comp in competencies if
                                 self.strip_competency_name_for_comparison(comp.name) in job_add_competencies_stripped]
        return filtered_competencies

    def strip_competency_name_for_comparison(self, competency_name: str) -> str:
        return competency_name.lower().replace(" ", "").replace("-", "")

    def build_projects(self, competencies: List[Competency]):
        projects = self.get_projects()
        filtered_projects = self.filter_most_relevant_projects(projects, competencies)
        self.file_handler.write_projects_generated_to_file(filtered_projects)

    def filter_most_relevant_projects(self, projects, competencies):
        known_languages = {comp.name for comp in competencies}
        filtered_projects = [
            proj for proj in projects if
            len(set(proj.languages).union(known_languages)) > 0
        ]
        projects = sorted(filtered_projects, key=lambda x: x.commits, reverse=True)[:2]
        return projects

    def build_summary(self):
        job_desc = self.file_handler.read_job_description()
        job_positions = self.file_handler.get_background_job_positions()
        question = f"""
        give me a summary of how i can contribute to this job description.
        \n\n {job_desc} \n\n
        given my competencies personal traits and experiences.
        job positions: {job_positions}
        """
        summary = self.chatgpt_interface.ask_question(question)
        self.file_handler.write_summary_to_file(summary)

    def extract_competencies_from_job_description(self, job_description: str, competencies: List[Competency]) -> List[
        str]:
        question = f"""What are the competencies required for the job: 
        \n\n {job_description} \n\n 
        The competencies should be formatted as a single list of strings, such as ["python", "javascript"]
        if any of the competencies mentioned are semantically the same as the competencies in the list below, then use
        the values from the list below. 
        \n\n{",".join([comp.name for comp in competencies])}\n\n"""

        response = self.chatgpt_interface.ask_question(question)
        competencies = json.loads(response)
        if isinstance(competencies, list) and all(isinstance(comp, str) for comp in competencies):
            return competencies
        else:
            logger.error(f"Invalid response: {response}")
            return []

    def generate_competencies_from_job_positions(self, job_positions: List[JobPosition]) -> List[Competency]:
        competencies = defaultdict(lambda: {'last_used': 0, 'years_of_experience': 0})

        for job in job_positions:
            years_of_exp = (job.end_date - job.start_date).days / 365.25

            for tech in job.technologies:
                competencies[tech]['last_used'] = max(job.end_date.year, competencies[tech]['last_used'])
                competencies[tech]['years_of_experience'] += years_of_exp

        return [
            Competency(
                name=tech,
                level=0,
                last_used=data['last_used'],
                years_of_experience=math.ceil(data['years_of_experience'])
            ) for tech, data in competencies.items()
        ]

    def build_job_positions(self):
        job_positions = self.file_handler.get_background_job_positions()
        job_positions = sorted(job_positions, key=lambda x: x.start_date, reverse=True)[:5]
        self.file_handler.write_job_positions(job_positions)


if __name__ == '__main__':
    cv_content_builder = CVContentBuilder()
    cv_content_builder.build_all()
