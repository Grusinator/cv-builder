import json
import math
import os
from typing import List
from collections import defaultdict
from datetime import datetime
import csv

from dotenv import load_dotenv

from cv_compiler.github_projects import GitHubProjectFetcher
from cv_compiler.llm_connector import ChatGPTInterface
from cv_compiler.models import JobPosition, Competency, GithubProject

JOB_POSITIONS_JSON = 'data/job_positions.json'
COMPETENCY_MATRIX_CSV = 'data/competency_matrix_initial.csv'

load_dotenv()


class CVContentBuilder:

    def __init__(self):
        self.github_fetcher = GitHubProjectFetcher(os.getenv('GITHUB_TOKEN'))
        self.chatgpt_interface = ChatGPTInterface(os.getenv('OPENAI_API_KEY'))

    def build_all(self):
        jobs = self.get_job_positions()
        competencies = self.generate_competencies_from_job_positions(jobs)
        self.write_competencies_generated(competencies)
        projects = self.get_projects()
        self.write_projects(projects)
        job_desc = self.read_job_description()
        exp_competencies = self.extract_competencies_from_job_description(job_desc)
        print(exp_competencies)

    def extract_competencies_from_job_description(self, job_description: str) -> List[str]:
        question = f"""What are the competencies required for the job: 
        \n\n {job_description} \n\n 
        formatted as a json list?"""
        response = self.chatgpt_interface.ask_question(question)
        return json.load(response)

    def get_projects(self):
        return self.github_fetcher.fetch_all()

    def calculate_competencies_matrix(self):
        jobs = self.get_job_positions()
        competencies = self.generate_competencies_from_job_positions(jobs)

    def get_job_positions(self) -> List[JobPosition]:
        # Load job positions from a JSON file manually
        with open(JOB_POSITIONS_JSON, 'r') as f:
            data = json.load(f)

            # Parse the data into Pydantic models
            job_positions = []
            for item in data:
                if item['end_date'] == 'Present':
                    item['end_date'] = datetime.now().isoformat()
                job_positions.append(JobPosition.parse_obj(item))

            return job_positions

    def load_competencies_from_csv(self) -> List[Competency]:
        competencies = []
        with open(COMPETENCY_MATRIX_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                competency = Competency.parse_obj(row)
                competencies.append(competency)
        return competencies

    def generate_competencies_from_job_positions(self, job_positions: List[JobPosition]) -> List[Competency]:
        competencies = defaultdict(lambda: {'LastUsed': 0, 'YearsOfExp': 0})

        for job in job_positions:
            years_of_exp = (job.end_date - job.start_date).days / 365.25

            for tech in job.technologies:
                competencies[tech]['LastUsed'] = max(job.end_date.year, competencies[tech]['LastUsed'])
                competencies[tech]['YearsOfExp'] += years_of_exp

        return [
            Competency(
                Category='Technologies',
                WorkingArea=tech,
                Level=0,
                LastUsed=data['LastUsed'],
                YearsOfExp=math.ceil(data['YearsOfExp'])
            ) for tech, data in competencies.items()
        ]

    def write_competencies_generated(self, competencies: List[Competency]):
        with open('data/competencies_generated.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Competency.__fields__.keys())
            writer.writeheader()
            for competency in competencies:
                writer.writerow(competency.dict())

    def write_projects(self, projects: List[GithubProject]):
        with open('data/projects.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=projects[0].__fields__.keys())
            writer.writeheader()
            for project in projects:
                writer.writerow(project.dict())

    def read_job_description(self):
        with open('data/job_description.txt', 'r') as f:
            job_description = f.read()
            return job_description


if __name__ == '__main__':
    cv_content_builder = CVContentBuilder()
    # cv_content_builder.calculate_competencies_matrix()
    # jobs = cv_content_builder.get_job_positions()
    # print(jobs)
    # competencies = cv_content_builder.generate_competencies_from_job_positions(jobs)
    # cv_content_builder.write_competencies_generated(competencies)
    #
    # # print(competencies)
    # projects = cv_content_builder.get_projects()
    # cv_content_builder.write_projects(projects)
    #
    job_desc = cv_content_builder.read_job_description()
    exp_competencies = cv_content_builder.extract_competencies_from_job_description(job_desc)
    print(exp_competencies)
