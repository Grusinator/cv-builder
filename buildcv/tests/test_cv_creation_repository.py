import pytest

from buildcv.repositories.cv_creation_repository import CvCreationRepository


@pytest.mark.django_db
def test_get_cv_creation_content(user, cv_creation_process, job_positions_in_db, projects_in_db,
                                 competencies_in_db, educations_in_db, job_post_in_db):
    repository = CvCreationRepository()
    cv_content = repository.get_cv_creation_content(user, job_post_in_db)

    assert cv_content.summary == 'Summary of the CV'

    assert len(cv_content.job_positions) == 5
    assert cv_content.job_positions[0].title == job_positions_in_db[0].title
    assert cv_content.job_positions[1].title == job_positions_in_db[1].title

    assert len(cv_content.projects) == 5
    assert cv_content.projects[0].name == projects_in_db[0].name
    assert cv_content.projects[1].name == projects_in_db[1].name

    assert len(cv_content.educations) == 5
    assert cv_content.educations[0].school == educations_in_db[0].school
    assert cv_content.educations[1].school == educations_in_db[1].school

    assert len(cv_content.competencies) == 5
    assert cv_content.competencies[0].name == competencies_in_db[0].name
    assert cv_content.competencies[1].name == competencies_in_db[1].name
