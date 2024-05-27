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
    def level_value(self):
        level_mapping = {
            'Some knowledge': 1,
            'Knowledgable': 2,
            'Experienced': 3,
            'Highly experienced': 4,
            'Expert': 5
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
