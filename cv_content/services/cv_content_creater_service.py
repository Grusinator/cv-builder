from typing import List

from loguru import logger

from cv_content.services.extract_cv_content_from_pdf_service import ExtractCvContentFromPdfService
from cv_content.services.competency_matrix_calculator_service import CompetencyMatrixCalculatorService
from cv_content.repositories.github_projects_repository import GitHubProjectsRepository
from cv_content.schemas import Competency
from cv_compiler.pdf_reader import PdfReader
from cv_content.repositories import CvContentRepository


class CVContentCreaterService:

    def __init__(self, repository=CvContentRepository()):
        self.repository: CvContentRepository = repository
        self.content_builder = ExtractCvContentFromPdfService()
        self.github_fetcher = GitHubProjectsRepository()
        self.competency_calculator = CompetencyMatrixCalculatorService()

    def fetch_github_projects(self, user, github_username, github_token):
        logger.info("Fetching GitHub projects")
        self.github_fetcher.username = github_username
        self.github_fetcher.token = github_token
        projects = self.github_fetcher.get_projects()
        projects = [project.map_to_generic_project() for project in projects]
        logger.debug(f"Fetched {len(projects)} projects from GitHub")
        return self.repository.create_projects(user, projects)

    def build_competencies_from_projects_and_jobs(self, user):
        job_positions = self.repository.get_job_positions(user=user)
        projects = self.repository.get_projects(user=user)
        existing_competencies = self.repository.get_competencies(user=user)
        competencies = self.competency_calculator.build(job_positions, projects, existing_competencies)
        new_competencies = [comp for comp in competencies if
                            comp not in existing_competencies and comp.competency_id is None]
        existing_competencies = [comp for comp in competencies if
                                 comp in existing_competencies and comp.competency_id is not None]
        new_competencies = self.repository.create_competencies(user, new_competencies)
        existing_competencies = self.repository.update_competencies(user, existing_competencies)
        return sorted(existing_competencies + new_competencies, key=lambda x: x.name)

    def match_competencies_with_job_description(self, competencies: List[Competency], job_description: str, n=15):
        return self.competency_calculator.find_most_relevant_competencies_to_job_add(job_description, competencies, n=n)

    def load_job_positions_from_pdf(self, user, pdf_bytes: bytes):
        pdf_cv_content = PdfReader().extract_text_from_pdf(pdf_bytes)
        job_positions = self.content_builder.get_job_positions_from_pdf(pdf_cv_content)
        self.repository.create_job_positions(user, job_positions)
        return job_positions

    def load_educations_from_pdf(self, user, pdf_bytes: bytes):
        pdf_cv_content = PdfReader().extract_text_from_pdf(pdf_bytes)
        educations = self.content_builder.get_educations_from_pdf(pdf_cv_content)
        self.repository.create_educations(user, educations)
        return educations
