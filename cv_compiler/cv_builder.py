from typing import List

from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.build_latex_content_files import LatexContentBuilder
import subprocess

from loguru import logger

from cv_compiler.competency_matrix_calculator import CompetencyMatrixCalculator
from cv_compiler.file_handler import FileHandler
from cv_compiler.github_project_fetcher import GitHubProjectFetcher
from cv_compiler.models import GithubProject, JobApplication, JobPosition, Competency, CvContent
from cv_compiler.pdf_reader import PdfReader


class CVCompiler:
    output_pdf_path = "main.pdf"

    def __init__(self, file_handler=FileHandler()):
        self.file_handler = file_handler
        self.content_builder = CVContentBuilder()
        self.github_fetcher = GitHubProjectFetcher()
        self.competency_calculator = CompetencyMatrixCalculator()
        self.latex_content_builder = LatexContentBuilder()

    def fetch_github_projects(self, github_username, github_token):
        logger.info("Fetching GitHub projects")
        self.github_fetcher.username = github_username
        self.github_fetcher.token = github_token
        projects = self.github_fetcher.get_projects()
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
        if result.returncode != 1 and "Error" in result.stderr:
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
        background_competencies = []
        job_app = JobApplication(company_name="", job_description=job_application_text)
        return self.competency_calculator.build(job_positions, projects, job_app, background_competencies)

    def match_competencies_with_job_description(self, competencies: List[Competency], job_description: str, n=15):
        return self.competency_calculator.find_most_relevant_competencies_to_job_add(job_description, competencies, n=n)

    def match_projects_with_competencies(self, projects: List[GithubProject], competencies: List[Competency]):
        return self.content_builder.filter_most_relevant_projects(projects, competencies)

    def load_job_positions_and_education_from_pdf(self, pdf_bytes: bytes):
        pdf_cv_content = PdfReader().extract_text_from_pdf(pdf_bytes)
        job_positions = self.content_builder.get_job_positions_from_pdf(pdf_cv_content)
        education = self.content_builder.get_education_from_pdf(pdf_cv_content)
        return job_positions, education

    def generate_summary(self, job_description: str, job_positions: List[JobPosition], educations, projects):
        return self.content_builder.generate_summary_from_llm(job_description, job_positions, educations, projects)
    
    def save_competencies(self, competencies: List[Competency]):
        self.file_handler.write_competency_matrix_generated(competencies)

    def get_competencies(self):
        return self.file_handler.read_generated_competencies_from_csv()


if __name__ == '__main__':
    cv_compiler = CVCompiler()
