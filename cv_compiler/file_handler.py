import csv
import json
from typing import List, Type

from pydantic import BaseModel

from cv_compiler.models import JobPosition, Competency, GithubProject

# data background

DATA_JOB_DESCRIPTION_TXT = 'job_application_text.txt'
BACKGROUND_JOB_POSITIONS_JSON = 'data_background/job_positions.json'
COMPETENCY_MATRIX_CSV = 'data_background/competency_matrix_initial.csv'


# data generated
GENERATED_PROJECTS_JSON = 'data_generated/projects.json'
GENERATED_COMPETENCY_MATRIX_CSV_FILE = 'data_generated/competencies.csv'
GENERATED_SUMMARY_TXT_FILE = 'data_generated/summary.txt'
GENERATED_JOB_POSITIONS = 'data_generated/job_positions.json'


class FileHandler:

    def read_generated_competencies_from_csv(self) -> List[Competency]:
        return self._read_from_csv(GENERATED_COMPETENCY_MATRIX_CSV_FILE, Competency)
    
    def _read_from_csv(self, file_path: str, cls):
        data = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                obj = cls.model_validate(row)
                data.append(obj)
        return data

    def write_competency_matrix_generated(self, competencies: List[Competency]):
        with open(GENERATED_COMPETENCY_MATRIX_CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Competency.__fields__.keys())
            writer.writeheader()
            for competency in competencies:
                writer.writerow(competency.dict())

    def get_background_job_positions(self) -> List[JobPosition]:
        return self._read_pydantic_objects_from_json(JobPosition, BACKGROUND_JOB_POSITIONS_JSON)

    def _read_pydantic_objects_from_json(self, cls, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
            return [cls.parse_obj(item) for item in data]

    def write_projects_generated_to_file(self, projects: List[GithubProject]):
        self._write_pydantic_objects_to_json_file(projects, GENERATED_PROJECTS_JSON)

    def read_job_description(self):
        with open(DATA_JOB_DESCRIPTION_TXT, 'r') as f:
            job_description = f.read()
            return job_description

    def _write_to_txt_file(self, output_file, content):
        with open(output_file, 'w+') as file:
            file.write(content)

    def write_summary_to_file(self, summary):
        self._write_to_txt_file(GENERATED_SUMMARY_TXT_FILE, summary)

    def read_summary_txt_file(self):
        with open(GENERATED_SUMMARY_TXT_FILE, 'r') as file:
            summary_text = file.read().replace('\n', ' ')
            return summary_text

    def read_generated_projects_from_csv(self):
        return self._read_pydantic_objects_from_json(GithubProject, GENERATED_PROJECTS_JSON)

    def write_job_positions(self, job_positions: List[JobPosition]):
        self._write_pydantic_objects_to_json_file(job_positions, GENERATED_JOB_POSITIONS)

    def _write_pydantic_objects_to_json_file(self, objects: List[BaseModel], file_path: str):
        with open(file_path, 'w') as f:
            json.dump([json.loads(obj.model_dump_json()) for obj in objects], f, indent=2)
