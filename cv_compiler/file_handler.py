import csv
import json
from datetime import datetime
from typing import List

import pandas as pd

from cv_compiler.models import JobPosition, Competency, GithubProject


# data background
GENERATED_CSV = 'data/competencies_generated.csv'

DATA_PROJECTS_CSV = 'data/projects.csv'

GENERATED_SUMMARY_TXT_FILE = 'data_generated/summary.txt'

DATA_JOB_DESCRIPTION_TXT = 'job_application_text.txt'
JOB_POSITIONS_JSON = 'data/job_positions.json'
COMPETENCY_MATRIX_CSV = 'data/competency_matrix_initial.csv'

# data generated

default_csv_file = 'data/competencies_old.csv'

job_application_text_file = 'job_application_text.txt'

class FileHandler:

    def read_competencies_csv_file(self, csv_file_path) -> pd.DataFrame:
        table_data = pd.read_csv(csv_file_path)
        return table_data

    def write_to_file(self, output_file, content):
        with open(output_file, 'w+') as file:
            file.write(content)
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

    def write_competencies_generated(self, competencies: List[Competency]):
        with open(GENERATED_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Competency.__fields__.keys())
            writer.writeheader()
            for competency in competencies:
                writer.writerow(competency.dict())

    def write_projects_to_file(self, projects: List[GithubProject]):
        with open(DATA_PROJECTS_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=projects[0].__fields__.keys())
            writer.writeheader()
            for project in projects:
                writer.writerow(project.dict())

    def read_job_description(self):
        with open(DATA_JOB_DESCRIPTION_TXT, 'r') as f:
            job_description = f.read()
            return job_description

    def write_summary_to_file(self, summary):
        self.write_to_file(GENERATED_SUMMARY_TXT_FILE, summary)
