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


class Competency(BaseModel):
    name: str  # Name?
    level: int
    category: Optional[str] = None
    last_used: int
    years_of_experience: int

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
    number_of_weeks_with_commits: Optional[int] = None
    last_commit: datetime
    languages: Optional[List[str]] = []
    technologies: Optional[List[str]] = []

    def map_to_generic_project(self) -> 'GenericProject':
        return GenericProject(
            name=self.name,
            description='',
            effort_in_years=self.number_of_weeks_with_commits / 52,
            competencies=self.technologies + self.languages
        )


class GenericProject(BaseModel):
    name: str
    description: str
    effort_in_years: float
    competencies: List[str] = []
