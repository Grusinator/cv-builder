import csv
import json
from datetime import datetime
from typing import List

import pandas as pd

from cv_compiler.models import JobPosition, Competency, GithubProject


# data background

DATA_JOB_DESCRIPTION_TXT = 'job_application_text.txt'
BACKGROUND_JOB_POSITIONS_JSON = 'data_background/job_positions.json'
COMPETENCY_MATRIX_CSV = 'data_background/competency_matrix_initial.csv'


# data generated
GENERATED_PROJECTS_CSV = 'data_generated/projects.csv'
GENERATED_COMPETENCY_MATRIX_CSV_FILE = 'data_generated/competencies.csv'
GENERATED_SUMMARY_TXT_FILE = 'data_generated/summary.txt'
GENERATED_JOB_POSITIONS = 'data_generated/job_positions.json'


class FileHandler:

    def read_generated_competencies_csv_file(self) -> pd.DataFrame:
        table_data = pd.read_csv(GENERATED_COMPETENCY_MATRIX_CSV_FILE)
        return table_data

    def read_generated_competencies_from_csv(self) -> List[Competency]:
        competencies = []
        with open(GENERATED_COMPETENCY_MATRIX_CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                competency = Competency.parse_obj(row)
                competencies.append(competency)
        return competencies

    def write_competency_matrix_generated(self, competencies: List[Competency]):
        with open(GENERATED_COMPETENCY_MATRIX_CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Competency.__fields__.keys())
            writer.writeheader()
            for competency in competencies:
                writer.writerow(competency.dict())

    def get_job_positions(self) -> List[JobPosition]:
        # Load job positions from a JSON file manually
        with open(BACKGROUND_JOB_POSITIONS_JSON, 'r') as f:
            data = json.load(f)

            # Parse the data into Pydantic models
            job_positions = []
            for item in data:
                if item['end_date'] == 'Present':
                    item['end_date'] = datetime.now().isoformat()
                job_positions.append(JobPosition.parse_obj(item))

            return job_positions

    def write_projects_generated_to_file(self, projects: List[GithubProject]):
        with open(GENERATED_PROJECTS_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=projects[0].__fields__.keys())
            writer.writeheader()
            for project in projects:
                writer.writerow(project.dict())

    def read_job_description(self):
        with open(DATA_JOB_DESCRIPTION_TXT, 'r') as f:
            job_description = f.read()
            return job_description

    def _write_to_file(self, output_file, content):
        with open(output_file, 'w+') as file:
            file.write(content)

    def write_summary_to_file(self, summary):
        self._write_to_file(GENERATED_SUMMARY_TXT_FILE, summary)

    def read_summary_txt_file(self):
        with open(GENERATED_SUMMARY_TXT_FILE, 'r') as file:
            summary_text = file.read().replace('\n', ' ')
            return summary_text

    def read_generated_projects_from_csv(self):
        projects = []
        with open(GENERATED_PROJECTS_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                project = GithubProject.parse_obj(row)
                projects.append(project)
        return projects
