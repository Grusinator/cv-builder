# tests/conftest.py
import json
from typing import Type

import pytest
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import AutoField, Model, JSONField
from mixer.backend.django import mixer
from mixer.main import GenFactory

from buildcv.models import JobPost, CvCreationProcess
from cv_content.models import ProjectModel, CompetencyModel, EducationModel, JobPositionModel

from mixer.backend.django import mixer as _mixer
from django.db.models import AutoField

from cv_content.schemas import JobPosition, Project, Education, Competency


# Function to reset auto fields to None
def reset_auto_fields_to_none(obj):
    for field in obj._meta.fields:
        if isinstance(field, AutoField):
            setattr(obj, field.name, None)
        elif isinstance(field, JSONField):
            setattr(obj, field.name, [])
    return obj


def _object_in_db(model: Type[Model], n=5, **kwargs):
    obs = [reset_auto_fields_to_none(_mixer.blend(model, **kwargs)) for _ in range(n)]
    obs = model.objects.bulk_create(obs)
    return obs


@pytest.fixture
def user():
    user = mixer.blend(User)
    user.save()
    return user


@pytest.fixture
def cv_creation_process(user, job_positions_in_db, projects_in_db, competencies_in_db, educations_in_db,
                        job_post_in_db):

    job_positions_json = JobPosition.dict_from_orm_list(job_positions_in_db)
    projects_json = Project.dict_from_orm_list(projects_in_db)
    educations_json = Education.dict_from_orm_list(educations_in_db)
    competencies_json = Competency.dict_from_orm_list(competencies_in_db)

    return CvCreationProcess.objects.create(
        user=user,
        job_post=job_post_in_db,
        job_positions=job_positions_json,
        projects=projects_json,
        educations=educations_json,
        competencies=competencies_json,
        summary='Summary of the CV'
    )


@pytest.fixture
def job_post_in_db(user):
    return _object_in_db(JobPost, user=user, n=1)[0]


@pytest.fixture
def job_positions_in_db(user):
    return _object_in_db(JobPositionModel, user=user, competencies=[])


@pytest.fixture
def projects_in_db(user):
    return _object_in_db(ProjectModel, user=user, competencies=[])


@pytest.fixture
def competencies_in_db(user):
    return _object_in_db(CompetencyModel, user=user)


@pytest.fixture
def educations_in_db(user):
    return _object_in_db(EducationModel, user=user)
