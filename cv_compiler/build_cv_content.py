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


class CVContentBuilder:

    def __init__(self):
        self.file_handler = FileHandler()
        self.github_fetcher = GitHubProjectFetcher()
        self.chatgpt_interface = ChatGPTInterface()
        self._projects = []

    def build_all(self):
        relevant_competencies = self.get_competencies_from_job_desciption_subset_of_job_positions()
        self.build_competency_matrix(relevant_competencies)
        self.build_projects(relevant_competencies)
        self.build_summary()
        self.build_job_positions()

    def get_projects(self):
        if len(self._projects) == 0:
            self._projects = self.github_fetcher.fetch_all()
        return self._projects

    def build_competency_matrix(self, competencies):
        self.file_handler.write_competency_matrix_generated(competencies)

    def get_competencies_from_job_desciption_subset_of_job_positions(self):
        jobs = self.file_handler.get_job_positions()
        competencies = self.generate_competencies_from_job_positions(jobs)
        job_description = self.file_handler.read_job_description()
        job_competencies = self.extract_competencies_from_job_description(job_description, competencies)
        filtered_competencies = [comp for comp in competencies if comp.WorkingArea in job_competencies]
        return filtered_competencies

    def build_projects(self, competencies: List[Competency]):
        projects = self.get_projects()
        filtered_projects = self.filter_most_relevant_projects(projects, competencies)
        self.file_handler.write_projects_generated_to_file(filtered_projects)

    def filter_most_relevant_projects(self, projects, competencies):
        known_languages = {comp.WorkingArea for comp in competencies}
        filtered_projects = [
            proj for proj in projects if
            len(set(proj.languages).union(known_languages)) > 0
        ]
        projects = sorted(filtered_projects, key=lambda x: x.commits, reverse=True)[:2]
        return projects

    def build_summary(self):
        job_desc = self.file_handler.read_job_description()
        job_positions = self.file_handler.get_job_positions()
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
        formatted as a json List[str], make it short and concise, if possible, select from this list: 
        \n\n{",".join([comp.WorkingArea for comp in competencies])}\n\n"""
        response = self.chatgpt_interface.ask_question(question)
        return json.loads(response)

    def generate_competencies_from_job_positions(self, job_positions: List[JobPosition]) -> List[Competency]:
        competencies = defaultdict(lambda: {'LastUsed': 0, 'YearsOfExp': 0})

        for job in job_positions:
            years_of_exp = (job.end_date - job.start_date).days / 365.25

            for tech in job.technologies:
                competencies[tech]['LastUsed'] = max(job.end_date.year, competencies[tech]['LastUsed'])
                competencies[tech]['YearsOfExp'] += years_of_exp

        return [
            Competency(
                WorkingArea=tech,
                Level=0,
                LastUsed=data['LastUsed'],
                YearsOfExp=math.ceil(data['YearsOfExp'])
            ) for tech, data in competencies.items()
        ]

    def build_job_positions(self):
        job_positions = self.file_handler.get_job_positions()
        job_positions = sorted(job_positions, key=lambda x: x.start_date, reverse=True)[:5]
        self.file_handler.write_job_positions(job_positions)


if __name__ == '__main__':
    cv_content_builder = CVContentBuilder()
    cv_content_builder.build_all()
