from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

from cv_content.schemas import JobPosition, Competency, GithubProject, Education


class BuildConfiguration(BaseModel):
    pass


class JobApplication(BaseModel):
    company_name: str
    job_description: str


@dataclass
class CvContent:
    job_positions: List[JobPosition]
    github_projects: List[GithubProject]
    educations: List[Education]
    competences: List[Competency]
    summary: str
