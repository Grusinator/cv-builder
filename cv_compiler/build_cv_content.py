from typing import List

from dotenv import load_dotenv

from cv_compiler.competency_matrix_calculator import CompetencyMatrixCalculator
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
        self.matrix_calc = CompetencyMatrixCalculator(self.chatgpt_interface)
        self._projects = []
        self._job_positions = []
        self._competencies = []
        self.job_description = []

    def build_all(self):
        relevant_competencies = self.build_competency_matrix_to_job_application()
        self.build_job_positions(relevant_competencies)
        self.build_projects(relevant_competencies)
        self.build_competency_matrix(relevant_competencies)
        self.build_summary()

    def build_competency_matrix_to_job_application(self):
        jobs = self.file_handler.get_background_job_positions()
        background_competencies = self.file_handler.get_background_competency_matrix()
        job_application = self.file_handler.read_job_application()
        projects = self.github_fetcher.fetch_all()
        filtered_competencies = self.matrix_calc.build(jobs, projects, job_application, background_competencies)
        return filtered_competencies

    def get_projects(self):
        if len(self._projects) == 0:
            self._projects = self.github_fetcher.fetch_all()
        return self._projects

    def build_competency_matrix(self, competencies):
        self.file_handler.write_competency_matrix_generated(competencies)

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
        job_desc = self.file_handler.read_job_application()
        job_positions = self.file_handler.get_background_job_positions()
        question = f"""
        Write a intro phrase for my cv of how i can contribute to this job. 4 lines of why im a good fit for this job.
        ------------------
         {job_desc} 
        ------------------
        consider the following job positions:
        {job_positions}
        ------------------
        make it short. its for a cv intro section. max 4 sentences.
        """
        summary = self.chatgpt_interface.ask_question(question)
        logger.debug(f"Summary: {summary}")
        self.file_handler.write_summary_to_file(summary)

    def build_job_positions(self, competencies):
        job_positions = self.file_handler.get_background_job_positions()
        job_positions = sorted(job_positions, key=lambda x: x.start_date, reverse=True)[:5]
        job_positions_w_relevant_competencies = [self.filter_for_relevant_competencies(job, competencies) for
                                                 job in job_positions]
        self.file_handler.write_job_positions(job_positions_w_relevant_competencies)

    def filter_for_relevant_competencies(self, job: JobPosition, competencies: List[Competency]) -> JobPosition:
        competency_names = [comp.name for comp in competencies]
        job.technologies = [tech for tech in job.technologies if tech in competency_names]
        return job


if __name__ == '__main__':
    cv_content_builder = CVContentBuilder()
    cv_content_builder.build_all()
