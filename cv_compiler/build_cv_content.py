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
        self.build_competency_matrix()
        self.build_projects()
        self.build_summary()

        jobs = self.file_handler.get_job_positions()
        competencies = self.generate_competencies_from_job_positions(jobs)
        self.file_handler.write_competency_matrix_generated(competencies)
        projects = self.get_projects()
        self.file_handler.write_projects_generated_to_file(projects)
        job_desc = self.file_handler.read_job_description()
        exp_competencies = self.extract_competencies_from_job_description(job_desc, competencies)
        print(exp_competencies)

    def get_projects(self):
        if len(self._projects) == 0:
            self._projects = self.github_fetcher.fetch_all()
        return self._projects

    def build_competency_matrix(self):
        jobs = self.file_handler.get_job_positions()
        competencies = self.generate_competencies_from_job_positions(jobs)
        self.file_handler.write_competency_matrix_generated(competencies)

    def build_projects(self):
        projects = self.get_projects()
        # filter most relevant projects
        self.file_handler.write_projects_generated_to_file(projects)

    def build_summary(self):
        job_desc = self.file_handler.read_job_description()
        job_experiences = self.get_projects()
        question = f"""
        give me a summary of how i can contribute to this job description.
        \n\n {job_desc} \n\n
        given my competencies personal traits and experiences.
        job experiences: {job_experiences}
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


if __name__ == '__main__':
    cv_content_builder = CVContentBuilder()
    cv_content_builder.build_all()
