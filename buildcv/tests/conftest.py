# tests/conftest.py

import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from cv_content.models import ProjectModel, CompetencyModel, EducationModel, JobPositionModel
from buildcv.models import JobPost, CvCreationProcess


@pytest.fixture
def user():
    return mixer.blend(User)


@pytest.fixture
def job_post(user):
    return mixer.blend(JobPost, user=user)


@pytest.fixture
def cv_creation(user, job_post):
    return CvCreationProcess.objects.create(
        user=user,
        job_post=job_post,
        summary='',
        projects=[],
        competencies=[],
        job_positions=[],
        educations=[]
    )


@pytest.fixture
def job_positions(user):
    obs = [mixer.blend(JobPositionModel, user=user, job_position_id=i) for i in range(5)]
    return obs


@pytest.fixture
def projects(user):
    return [mixer.blend(ProjectModel, user=user, competencies=[]) for _ in range(5)]


@pytest.fixture
def competencies(user):
    return [mixer.blend(CompetencyModel, user=user) for _ in range(5)]


@pytest.fixture
def educations(user):
    return [mixer.blend(EducationModel, user=user) for _ in range(5)]
