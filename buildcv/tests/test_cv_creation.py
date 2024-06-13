import pytest
from django.contrib.messages import get_messages
from django.core.serializers import serialize
from django.urls import reverse

from buildcv.models import CvCreationProcess
from cv_content.models import JobPositionModel, CompetencyModel, ProjectModel, EducationModel

import mixer

from cv_content.schemas import Project, Education, Competency


@pytest.mark.django_db
class TestCvCreationViews:

    def test_manage_summary_get(self, client, user, job_post_in_db, cv_creation_process):
        client.force_login(user)
        url = reverse('manage_summary', kwargs={'job_post_id': job_post_in_db.job_post_id})
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_generate_summary(self, client, mocker, user, job_post_in_db, projects, competencies, educations):
        mock_generate_summary = mocker.patch('buildcv.services.GenerateSummaryService.generate_summary_from_llm')
        mock_generate_summary.return_value = 'Generated summary from mock service.'

        client.force_login(user)
        url = reverse('generate_summary', kwargs={'job_post_id': job_post_in_db.job_post_id})
        response = client.post(url)

        assert response.status_code == 302
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == 'Summary generated successfully.'
        cv_creation_process = CvCreationProcess.objects.get(user=user, job_post=job_post_in_db)
        assert cv_creation_process.summary == 'Generated summary from mock service.'

    def test_manage_summary_post_save(self, client, user, job_post_in_db, cv_creation_process):
        client.force_login(user)
        url = reverse('manage_summary', kwargs={'job_post_id': job_post_in_db.job_post_id})
        data = {
            'summary': 'This is a generated summary.',
            'save_summary': 'true'
        }
        response = client.post(url, data=data)
        assert response.status_code == 302
        cv_creation_process.refresh_from_db()
        assert cv_creation_process.summary == 'This is a generated summary.'

    def test_manage_content_selection_get(self, client, user, job_post_in_db, cv_creation_process, competencies_in_db,
                                          projects_in_db, educations_in_db, job_positions_in_db):
        client.force_login(user)
        url = reverse('manage_content_selection', kwargs={'job_post_id': job_post_in_db.job_post_id})
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_manage_content_selection_post(self, client, user, job_post_in_db, projects_in_db, competencies_in_db,
                                           educations_in_db, job_positions_in_db):
        client.force_login(user)
        data = {
            'projects': [project.project_id for project in projects_in_db],
            'competencies': [competency.competency_id for competency in competencies_in_db],
            'job_positions': [job_position.job_position_id for job_position in job_positions_in_db],
            'educations': [education.education_id for education in educations_in_db]
        }
        url = reverse('manage_content_selection', kwargs={'job_post_id': job_post_in_db.job_post_id})

        response = client.post(url, job_post_id=job_post_in_db.job_post_id, data=data)
        assert response.status_code == 302
        cv_creation_process = CvCreationProcess.objects.get(user=user, job_post=job_post_in_db)
        assert Project.from_orm_list(projects_in_db) == [Project(**proj) for proj in cv_creation_process.projects]
        assert Competency.from_orm_list(competencies_in_db) == [Competency(**comp) for comp in
                                                                cv_creation_process.competencies]
        assert Education.from_orm_list(educations_in_db) == [Education(**edu) for edu in cv_creation_process.educations]
