import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from cv_content.models import EducationModel


@pytest.mark.django_db
class TestEducationViews:
    def test_add_education(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('add_education')
        data = {
            'degree': 'MSc Computer Science',
            'school': 'Tech University',
            'start_date': '2018-09-01',
            'end_date': '2020-06-01',
            'description': 'Studied advanced computer science topics.',
            'location': 'Tech City'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert EducationModel.objects.count() == 1

    def test_list_educations(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        mixer.cycle(3).blend(EducationModel, user=user)
        url = reverse('list_educations')
        response = client.get(url)
        assert response.status_code == 200
        assert 'educations' in response.context
        assert len(response.context['educations']) == 3

    def test_update_education(self, client):
        user = mixer.blend(User)
        education = mixer.blend(EducationModel, user=user)
        client.force_login(user)
        url = reverse('update_education', kwargs={'education_id': education.education_id})
        data = {
            'degree': 'Updated Degree',
            'school': 'New School',
            'start_date': '2020-01-01',
            'end_date': '2024-01-01',
            'description': 'Updated Description',
            'location': 'Updated Location'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        education.refresh_from_db()
        assert education.degree == 'Updated Degree'

    def test_delete_education(self, client):
        user = mixer.blend(User)
        education = mixer.blend(EducationModel, user=user)
        client.force_login(user)
        url = reverse('delete_education', kwargs={'education_id': education.education_id})
        response = client.post(url)
        assert response.status_code == 302
        assert EducationModel.objects.count() == 0
