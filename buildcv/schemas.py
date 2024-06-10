from typing import List

from pydantic import BaseModel

from cv_content.schemas import JobPosition, Competency, Education, Project


class BuildConfiguration(BaseModel):
    pass


class JobApplication(BaseModel):
    company_name: str
    job_description: str

    class Config:
        from_attributes = True


class CvContent(BaseModel):
    job_positions: List[JobPosition]
    projects: List[Project]
    educations: List[Education]
    competencies: List[Competency]
    summary: str

    class Config:
        from_attributes = True
