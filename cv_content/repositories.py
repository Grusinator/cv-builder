from typing import List

from django.contrib.auth.models import User
from django.db import transaction

from cv_compiler.models import JobPosition, Competency, Education, Project
from .models import JobPositionModel, CompetencyModel, ProjectModel, EducationModel


class CvContentRepository:

    @staticmethod
    def create_job_position(user: User, job_position: JobPosition) -> JobPosition:
        job_position = JobPositionModel.objects.create(**job_position.dict(), user=user)
        return JobPosition.from_orm(job_position)

    @staticmethod
    def get_job_positions(user: User) -> List[JobPosition]:
        return [JobPosition.from_orm(jp) for jp in JobPositionModel.objects.filter(user=user)]

    @staticmethod
    def update_job_position(job_position_id: int, data: dict) -> JobPosition:
        JobPositionModel.objects.filter(id=job_position_id).update(**data)
        return JobPosition.from_orm(JobPositionModel.objects.get(id=job_position_id))

    @staticmethod
    def delete_job_position(user: User, job_position_id: int):
        JobPositionModel.objects.get(user=user, job_position_id=job_position_id).delete()

    @staticmethod
    def create_competency(user: User, data: Competency) -> Competency:
        competency = CompetencyModel.objects.create(
            user=user,
            name=data.name,
            level=data.level,
            category=data.category,
            last_used=data.last_used,
            years_of_experience=data.years_of_experience,
            attractiveness=data.attractiveness
        )
        return Competency.from_orm(competency)

    @staticmethod
    def get_competencies(user: User) -> List[Competency]:
        return [Competency.from_orm(comp) for comp in CompetencyModel.objects.filter(user=user)]

    @staticmethod
    def create_project(user: User, data: Project) -> Project:
        project = ProjectModel.objects.create(
            user=user,
            name=data.name,
            owner=data.owner,
            commits=data.commits,
            description=data.description,
            number_of_weeks_with_commits=data.number_of_weeks_with_commits,
            last_commit=data.last_commit,
            topics=data.topics,
            languages=data.languages,
            technologies=data.technologies
        )
        return Project.from_orm(project)

    @staticmethod
    def get_projects(user: User) -> List[Project]:
        return [Project.from_orm(proj) for proj in ProjectModel.objects.filter(user=user)]

    @staticmethod
    def create_education(user: User, data: Education) -> Education:
        education = EducationModel.objects.create(
            user=user,
            degree=data.degree,
            school=data.school,
            start_date=data.start_date,
            end_date=data.end_date,
            description=data.description,
            location=data.location
        )
        return Education.from_orm(education)

    @staticmethod
    def delete_education(user: User, education_id: int):
        EducationModel.objects.get(education_id=education_id, user=user).delete()

    @staticmethod
    def get_educations(user: User) -> List[Education]:
        return [Education.from_orm(edu) for edu in EducationModel.objects.filter(user=user)]

    def update_education(self, education_id, data):
        EducationModel.objects.filter(id=education_id).update(**data)
        return data


    def create_competencies(self, user, competencies):
        with transaction.atomic():
            for competency in competencies:
                self.create_competency(user, competency)

    def create_educations(self, user, educations):
        with transaction.atomic():
            for education in educations:
                self.create_education(user, education)

    def create_job_positions(self, user, job_positions):
        with transaction.atomic():
            for job_position in job_positions:
                self.create_job_position(user, job_position)




