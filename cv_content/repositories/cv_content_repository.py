from typing import List

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import AutoField
from pydantic import BaseModel

from cv_content.schemas import JobPosition, Competency, Project, Education
from cv_content.models import JobPositionModel, CompetencyModel, ProjectModel, EducationModel


class CvContentRepository:

    @staticmethod
    def create_job_position(user: User, job_position: JobPosition) -> JobPosition:
        job_position.job_position_id = None
        job_position = JobPositionModel.objects.create(**job_position.dict(), user=user)
        return JobPosition.model_validate(job_position)

    @staticmethod
    def get_job_positions(user: User) -> List[JobPosition]:
        return [JobPosition.model_validate(jp) for jp in JobPositionModel.objects.filter(user=user)]

    @staticmethod
    def update_job_position(job_position_id: int, data: dict) -> JobPosition:
        JobPositionModel.objects.filter(id=job_position_id).update(**data)
        return JobPosition.model_validate(JobPositionModel.objects.get(id=job_position_id))

    @staticmethod
    def delete_job_position(user: User, job_position_id: int):
        JobPositionModel.objects.get(user=user, job_position_id=job_position_id).delete()

    @staticmethod
    def create_competency(user: User, data: Competency) -> Competency:
        data.competency_id = None
        competency = CompetencyModel.objects.create(user=user, **data.dict())
        return Competency.model_validate(competency)

    @staticmethod
    def get_competencies(user: User) -> List[Competency]:
        return [Competency.model_validate(comp) for comp in CompetencyModel.objects.filter(user=user)]

    def delete_competency(self, user, competency_id):
        CompetencyModel.objects.get(user=user, competency_id=competency_id).delete()

    @staticmethod
    def create_project(user: User, data: Project) -> Project:
        data.project_id= None
        project = ProjectModel.objects.create(user=user, **data.dict())
        return Project.model_validate(project)

    @staticmethod
    def get_projects(user: User) -> List[Project]:
        return [Project.model_validate(proj) for proj in ProjectModel.objects.filter(user=user)]

    @staticmethod
    def create_education(user: User, edu: Education) -> Education:
        edu.education_id = None
        education = EducationModel.objects.create(user=user, **edu.dict())
        return Education.model_validate(education)

    @staticmethod
    def delete_education(user: User, education_id: int):
        EducationModel.objects.get(education_id=education_id, user=user).delete()

    @staticmethod
    def get_educations(user: User) -> List[Education]:
        return [Education.model_validate(edu) for edu in EducationModel.objects.filter(user=user)]

    def create_educations(self, user, educations):
        with transaction.atomic():
            return [self.create_education(user, education) for education in educations]

    def update_education(self, education_id, data):
        EducationModel.objects.filter(id=education_id).update(**data)
        return data

    def create_competencies(self, user, competencies):
        with transaction.atomic():
            return [self.create_competency(user, competency) for competency in competencies]

    def create_job_positions(self, user, job_positions):
        with transaction.atomic():
            return [self.create_job_position(user, job_position) for job_position in job_positions]

    def create_projects(self, user, projects):
        with transaction.atomic():
            return [self.create_project(user, project) for project in projects]

    def update_competency(self, user: User, competency: Competency):
        competency_dict = competency.dict()
        competency_id = competency_dict.pop('competency_id')
        CompetencyModel.objects.filter(user=user, competency_id=competency_id).update(**competency_dict)
        return competency

    def update_competencies(self, user, competencies: List[Competency]):
        with transaction.atomic():
            return [self.update_competency(user, competency) for competency in competencies]