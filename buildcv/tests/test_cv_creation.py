import pytest
from django.contrib.messages import get_messages
from django.core.serializers import serialize
from django.urls import reverse

from buildcv.models import CvCreationProcess
from cv_content.models import JobPositionModel, CompetencyModel, ProjectModel, EducationModel


@pytest.mark.django_db
class TestCvCreationViews:

    def test_manage_summary_get(self, client, user, job_post, cv_creation):
        client.force_login(user)
        url = reverse('manage_summary', kwargs={'job_post_id': job_post.job_post_id})
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_generate_summary(self, client, mocker, user, job_post, projects, competencies, educations):
        mock_generate_summary = mocker.patch('buildcv.services.GenerateSummaryService.generate_summary_from_llm')
        mock_generate_summary.return_value = 'Generated summary from mock service.'

        client.force_login(user)
        url = reverse('generate_summary', kwargs={'job_post_id': job_post.job_post_id})
        response = client.post(url)

        assert response.status_code == 302
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == 'Summary generated successfully.'
        cv_creation = CvCreationProcess.objects.get(user=user, job_post=job_post)
        assert cv_creation.summary == 'Generated summary from mock service.'

    def test_manage_summary_post_save(self, client, user, job_post, cv_creation):
        client.force_login(user)
        url = reverse('manage_summary', kwargs={'job_post_id': job_post.job_post_id})
        data = {
            'summary': 'This is a generated summary.',
            'save_summary': 'true'
        }
        response = client.post(url, data=data)
        assert response.status_code == 302
        cv_creation.refresh_from_db()
        assert cv_creation.summary == 'This is a generated summary.'

    def test_manage_content_selection_get(self, client, user, job_post, cv_creation):
        client.force_login(user)
        url = reverse('manage_content_selection', kwargs={'job_post_id': job_post.job_post_id})
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_manage_content_selection_post(self, client, user, job_post, projects, competencies, educations, job_positions):
        JobPositionModel.objects.bulk_create(job_positions)
        EducationModel.objects.bulk_create(educations)
        ProjectModel.objects.bulk_create(projects)
        CompetencyModel.objects.bulk_create(competencies)
        client.force_login(user)
        url = reverse('manage_content_selection', kwargs={'job_post_id': job_post.job_post_id})

        response = client.post(url, job_post_id=job_post.job_post_id)
        assert response.status_code == 302
        cv_creation = CvCreationProcess.objects.get(user=user, job_post=job_post)
        assert serialize('json', projects) == cv_creation.projects
        assert serialize('json', competencies) == cv_creation.competencies
        assert serialize('json', educations) == cv_creation.educations
