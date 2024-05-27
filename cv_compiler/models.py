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


class Competency(BaseModel):
    WorkingArea: str  # Name?
    Level: int
    Category: Optional[str] = None
    LastUsed: int
    YearsOfExp: int

    @property
    def level_description(self):
        level_mapping = {
            1: 'Some knowledge',
            2: 'Knowledgable',
            3: 'Experienced',
            4: 'Highly experienced',
            5: 'Expert'
        }
        return level_mapping.get(self.Level, None)


class GithubProject(BaseModel):
    name: str
    owner: str
    commits: int
    number_of_weeks_with_commits: int
    last_commit: datetime
    languages: List[str]
    technologies: List[str]
