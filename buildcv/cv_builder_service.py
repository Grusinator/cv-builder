from typing import List
from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.build_latex_content_files import LatexContentBuilder
import subprocess

from loguru import logger
from cv_compiler.competency_matrix_calculator import CompetencyMatrixCalculator
from cv_compiler.github_project_fetcher import GitHubProjectFetcher
from cv_compiler.models import GithubProject, JobApplication, JobPosition, Competency, CvContent
from cv_compiler.pdf_reader import PdfReader
from .cv_builder_repository import CvBuilderRepository


class CVBuilderService:
    output_pdf_path = "main.pdf"

    def __init__(self, repository=CvBuilderRepository()):
        self.repository = repository
        self.content_builder = CVContentBuilder()
        self.github_fetcher = GitHubProjectFetcher()
        self.competency_calculator = CompetencyMatrixCalculator()
        self.latex_content_builder = LatexContentBuilder()

    def fetch_github_projects(self, github_username, github_token):
        logger.info("Fetching GitHub projects")
        self.github_fetcher.username = github_username
        self.github_fetcher.token = github_token
        projects = self.github_fetcher.get_projects()
        for project in projects:
            self.repository.create_project(project)
        return projects

    def build_cv_from_content(self, selected_jobs, selected_education, selected_projects,
                              selected_competencies, summary):
        content = CvContent(job_positions=selected_jobs, github_projects=selected_projects,
                            educations=selected_education,
                            competences=selected_competencies, summary=summary)
        self.latex_content_builder.build_content(content)
        pdf_file = self.build_latex_cv()
        return pdf_file

    def build_latex_cv(self):
        command = "pdflatex -interaction=nonstopmode main.tex"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        logger.debug(result.stdout)
        logger.debug("return code: " + str(result.returncode))
        logger.debug(result.stderr)
        if result.returncode != 0:
            logger.error(result.stderr)
            raise Exception(f"Error building CV: \n {result.stderr}")
        else:
            logger.info("CV successfully built")
            return self.load_pdf()

    def load_pdf(self):
        with open(self.output_pdf_path, "rb") as f:
            return f.read()

    def build_competencies(self, job_application_text: str, job_positions: List[JobPosition],
                           projects: List[GithubProject]):
        job_app = JobApplication(company_name="", job_description=job_application_text)
        background_competencies = self.repository.get_competencies()
        return self.competency_calculator.build(job_positions, projects, job_app, background_competencies)

    def match_competencies_with_job_description(self, competencies: List[Competency], job_description: str, n=15):
        return self.competency_calculator.find_most_relevant_competencies_to_job_add(job_description, competencies, n=n)

    def match_projects_with_competencies(self, projects: List[GithubProject], competencies: List[Competency]):
        return self.content_builder.filter_most_relevant_projects(projects, competencies)

    def load_job_positions_and_education_from_pdf(self, pdf_bytes: bytes):
        pdf_cv_content = PdfReader().extract_text_from_pdf(pdf_bytes)
        job_positions = self.content_builder.get_job_positions_from_pdf(pdf_cv_content)
        educations = self.content_builder.get_educations_from_pdf(pdf_cv_content)
        self.repository.create_job_positions(user, job_positions)
        self.repository.create_educations(user, educations)
        return job_positions, educations

    def generate_summary(self, job_description: str, job_positions: List[JobPosition], educations, projects):
        return self.content_builder.generate_summary_from_llm(job_description, job_positions, educations, projects)

    def save_competencies(self, user, competencies: List[Competency]):
        self.repository.create_competencies(user, competencies)

    def get_competencies(self, user):
        return self.repository.get_competencies(user)

    def get_logged_in_user(self):
        return self.repository.get_logged_in_user()
