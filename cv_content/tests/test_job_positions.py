import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from cv_content.models import JobPositionModel

@pytest.mark.django_db
class TestJobPositionViews:
    def test_create_job_position(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('add_job_position')
        data = {
            'title': 'Software Engineer',
            'company': 'OpenAI',
            'location': 'San Francisco',
            'start_date': '2020-01-01',
            'end_date': '2022-01-01',
            'description': 'Work on AI models.',
            'competencies': 'Python, ML'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert JobPositionModel.objects.count() == 1

    def test_list_job_positions(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        mixer.cycle(5).blend(JobPositionModel, user=user)
        url = reverse('list_job_positions')
        response = client.get(url)
        assert response.status_code == 200
        assert 'job_positions' in response.context
        assert len(response.context['job_positions']) == 5

    def test_update_job_position(self, client):
        user = mixer.blend(User)
        job = mixer.blend(JobPositionModel, user=user)
        client.force_login(user)
        url = reverse('update_job_position', kwargs={'job_id': job.job_position_id})
        data = {
            'title': 'Updated Title',
            'company': 'Updated Company',
            'location': 'Updated Location',
            'start_date': '2020-01-01',  # Assuming this is required
            'end_date': '2024-01-01',  # Assuming this is required
            'description': 'Updated Description',  # Assuming this is required
            'competencies': 'Updated Competency1, Updated Competency2'  # Assuming this is required
        }
        response = client.post(url, data)
        assert response.status_code == 302
        job.refresh_from_db()
        assert job.title == 'Updated Title'

    def test_delete_job_position(self, client):
        user = mixer.blend(User)
        job = mixer.blend(JobPositionModel, user=user)
        client.force_login(user)
        url = reverse('delete_job_position', kwargs={'job_id': job.job_position_id})
        response = client.post(url)
        assert response.status_code == 302
        assert JobPositionModel.objects.count() == 0
