import io
import json
from typing import List

import pdfplumber
from dotenv import load_dotenv

from cv_compiler.competency_matrix_calculator import CompetencyMatrixCalculator
from cv_compiler.file_handler import FileHandler
from cv_compiler.github_project_fetcher import GitHubProjectFetcher
from cv_compiler.llm_connector import ChatGPTInterface
from cv_compiler.models import JobPosition, Competency, Education

load_dotenv()

from loguru import logger


class CVContentBuilder:

    def __init__(self, file_handler=FileHandler()):
        self.file_handler = file_handler
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
        education = self.file_handler.read_generated_educations()
        projects = self.file_handler.read_generated_projects_from_json()
        summary = self.generate_summary_from_llm(job_desc, job_positions, education, projects)
        self.file_handler.write_summary_to_file(summary)

    def generate_summary_from_llm(self, job_desc, job_positions, education, projects):
        question = f"""
        Write a intro phrase for my cv of how i can contribute to this job. 4 lines of why im a good fit for this job.
        Please dont overexaggerate, just be honest, based on what you know about me, jobs and projects,
        if im not a great fit, just say so, but be constructive, about other things that i can contribute with.
        Feel free to mention the company name and job title. 
        Here is the job post description. 
         {job_desc} 
        ------------------
        consider the following job positions:
        {job_positions}
        ------------------
        consider the following education:
        {education}
        ------------------
        consider the following projects:
        {projects}
        ------------------
        make it short. its for a cv intro section. max 4 sentences.
        """
        summary = self.chatgpt_interface.ask_question(question)
        logger.debug(f"Summary: {summary}")
        return summary

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

    def get_job_positions_from_pdf(self, pdf):
        logger.debug(f"Extracting job positions from pdf")
        pdf_content = self.extract_text_from_pdf(pdf)
        question = f"""
        Extract job positions from this pdf. it has to be stored in json format, with these fields, 
        please save dates as yyyy-mm-dd, just assume first in month if day is not given.
        {JobPosition.__fields__.keys()}
        Job positions can be found in the following text:
        ------------------
        {pdf_content}
        """
        return self.chatgpt_interface.ask_question_that_returns_pydantic_list(question, JobPosition)

    def extract_text_from_pdf(self, pdf_bytes):
        text = ''
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() if page.extract_text() else ''
        return text

    def get_education_from_pdf(self, pdf):

        pdf_content = self.extract_text_from_pdf(pdf)
        question = f"""
         Extract education from this pdf. it has to be stored in json format, with these fields:
         please save dates as yyyy-mm-dd, just assume first in month if day is not given.
         {Education.__fields__.keys()}
         Education can be found in the following text:
         ------------------
         {pdf_content}
         """
        return self.chatgpt_interface.ask_question_that_returns_pydantic_list(question, Education)


if __name__ == '__main__':
    cv_content_builder = CVContentBuilder()
    cv_content_builder.build_all()
