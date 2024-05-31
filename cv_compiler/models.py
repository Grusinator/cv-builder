from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class JobPosition(BaseModel):
    title: str
    company: str
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = []

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d')
        }

    @property
    def unique_id(self):
        return f"{self.company}-{self.start_date.strftime('%Y-%m-%d')}"


class Competency(BaseModel):
    name: str  # Name?
    level: int
    category: Optional[str] = None
    last_used: int
    years_of_experience: float
    attractiveness: Optional[int] = 0

    @property
    def level_description(self):
        level_mapping = {
            1: 'Some knowledge',
            2: 'Knowledgable',
            3: 'Experienced',
            4: 'Highly experienced',
            5: 'Expert'
        }
        return level_mapping.get(self.level, None)


class GithubProject(BaseModel):
    name: str
    owner: str
    commits: int
    description: Optional[str] = None
    number_of_weeks_with_commits: Optional[int] = None
    last_commit: datetime
    topics: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    technologies: Optional[List[str]] = []

    def map_to_generic_project(self) -> 'GenericProject':
        return GenericProject(
            name=self.name,
            description=self.description if self.description else '',
            effort_in_years=self.number_of_weeks_with_commits / 52,
            competencies=set(self.technologies + self.languages + self.topics)
        )


class GenericProject(BaseModel):
    name: str
    description: str
    effort_in_years: float
    competencies: List[str] = []


class BuildConfiguration(BaseModel):
    pass


class JobApplication(BaseModel):
    company_name: str
    job_description: str


class Education(BaseModel):
    degree: str
    school: str
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None
    location: Optional[str] = None
