import io
import json
from typing import List

import pdfplumber
from dotenv import load_dotenv

from cv_compiler.competency_matrix_calculator import CompetencyMatrixCalculator
from cv_compiler.file_handler import FileHandler
from cv_compiler.github_project_fetcher import GitHubProjectFetcher
from cv_compiler.llm_connector import LlmConnector
from cv_compiler.models import JobPosition, Competency, Education, GithubProject

load_dotenv()

from loguru import logger


class CVContentBuilder:

    def __init__(self):
        self.chatgpt_interface = LlmConnector()

    def filter_most_relevant_projects(self, projects: List[GithubProject], competencies: List[Competency]):
        known_languages = {comp.name for comp in competencies}
        filtered_projects = [
            proj for proj in projects if
            len(set(proj.languages + proj.topics).intersection(known_languages)) > 0
        ]
        projects = sorted(filtered_projects, key=lambda x: x.commits, reverse=True)
        return projects

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

    def get_job_positions_from_pdf(self, cv_text_with_job_positions):
        question = f"""
        Extract job positions from this pdf. it has to be stored in json format, with these fields, 
        please save dates as yyyy-mm-dd, just assume first in month if day is not given.
        {JobPosition.__fields__.keys()}
        Job positions can be found in the following text:
        ------------------
        {cv_text_with_job_positions}
        """
        return self.chatgpt_interface.ask_question_that_returns_pydantic_list(question, JobPosition)

    def get_educations_from_pdf(self, cv_text_with_educations):
        question = f"""
         Extract education from this pdf. it has to be stored in json format, with these fields:
         please save dates as yyyy-mm-dd, just assume first in month if day is not given.
         {Education.__fields__.keys()}
         Education can be found in the following text:
         ------------------
         {cv_text_with_educations}
         """
        return self.chatgpt_interface.ask_question_that_returns_pydantic_list(question, Education)


if __name__ == '__main__':
    cv_content_builder = CVContentBuilder()
