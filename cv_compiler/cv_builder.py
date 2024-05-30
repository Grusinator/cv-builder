from typing import List

from cv_compiler.build_cv_content import CVContentBuilder
from cv_compiler.build_latex_content_files import LatexContentBuilder
import subprocess

from loguru import logger

from cv_compiler.file_handler import FileHandler
from cv_compiler.models import GithubProject


class CVCompiler:
    output_pdf_path = "main.pdf"

    def __init__(self, file_handler=FileHandler()):
        self.file_handler = file_handler
        self.content_builder = CVContentBuilder(self.file_handler)
        self.latex_builder = LatexContentBuilder(self.file_handler)

    def parse_job_application(self, job_application_text):
        logger.info("Parsing job application")
        logger.debug(f"job application: {job_application_text}")
        self.file_handler.write_job_application(job_application_text)

    def fetch_github_projects(self, github_username, github_token):
        logger.info("Fetching GitHub projects")
        self.content_builder.github_fetcher.username = github_username
        self.content_builder.github_fetcher.token = github_token
        projects = self.content_builder.get_projects()
        return projects

    def update_generated_projects(self, projects: List[GithubProject]):
        self.file_handler.write_projects_generated_to_file(projects)

    def build_cv(self):
        logger.info("Building CV")
        self.content_builder.build_all()
        self.latex_builder.build_all()
        pdf_file = self.build_latex_cv()
        return pdf_file

    def build_latex_cv(self):
        command = "pdflatex -interaction=nonstopmode main.tex"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        logger.debug(result.stdout)
        logger.debug("return code: " + str(result.returncode))
        logger.debug(result.stderr)
        if result.returncode != 1:
            logger.error(result.stderr)
            raise Exception(f"Error building CV: \n {result.stderr}")
        else:
            logger.info("CV successfully built")
            return self.load_pdf()

    def load_pdf(self):
        with open(self.output_pdf_path, "rb") as f:
            return f.read()

    def fetch_jobs(self):
        return self.file_handler.get_background_job_positions()

    def build_competencies(self, job_application_text, job_positions, projects):
        background_competencies = []
        return self.content_builder.matrix_calc.build(job_positions, projects, job_application_text,
                                                      background_competencies)


if __name__ == '__main__':
    cv_compiler = CVCompiler()
    cv_compiler.build_cv()
