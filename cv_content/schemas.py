import json
from datetime import datetime
from typing import Optional, List

from django.db.models import Model
from pydantic import BaseModel


class CustomBasePydanticModel(BaseModel):
    class Config:
        from_attributes = True  # This line is needed to use from_orm properly

        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d')
        }

    @classmethod
    def from_orm_list(cls, django_objects) -> List['CustomBasePydanticModel']:
        return [cls.model_validate(job) for job in django_objects]

    @classmethod
    def dict_from_orm_list(cls, django_objects: List[Model]) -> List[dict]:
        # back and forth to let the json_encoders work
        return [json.loads(cls.model_validate(obj).model_dump_json()) for obj in django_objects]


class JobPosition(CustomBasePydanticModel):
    job_position_id: Optional[int] = None
    title: str
    company: str
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    description: Optional[str] = None
    competencies: List[str] = []

    @property
    def unique_id(self):
        return f"{self.company}-{self.start_date.strftime('%Y-%m-%d')}"


class Competency(CustomBasePydanticModel):
    competency_id: Optional[int] = None
    name: str
    level: int
    category: Optional[str] = None
    last_used: int
    years_of_experience: float
    attractiveness: Optional[int] = 0

    class Config:
        from_attributes = True  # This line is needed to use from_orm properly

    @staticmethod
    def strip_competency_name_for_comparison(competency_name: str) -> str:
        return competency_name.lower().replace(" ", "").replace("-", "")

    @property
    def stripped_name(self):
        return self.strip_competency_name_for_comparison(self.name)

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

    def map_to_generic_project(self) -> 'Project':
        return Project(
            name=self.name,
            description=self.description if self.description else '',
            effort_in_years=float(max(0.1, self.number_of_weeks_with_commits or 0 / 47)),
            last_updated=self.last_commit,
            competencies=set(self.technologies + self.languages + self.topics)
        )


class Project(CustomBasePydanticModel):
    project_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    effort_in_years: float
    last_updated: datetime
    competencies: List[str] = []
    url: Optional[str] = None


class Education(CustomBasePydanticModel):
    education_id: Optional[int] = None
    degree: str
    school: str
    start_date: datetime
    end_date: datetime
    description: Optional[str] = None
    location: Optional[str] = None
