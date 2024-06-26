import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from mixer.backend.django import mixer

from cv_content.models import CompetencyModel
from cv_content.repositories import CvContentRepository


@pytest.mark.django_db
class TestCompetencyViews:
    def test_add_competency(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('add_competency')
        data = {
            'name': 'Python',
            'level': 5,
            'category': 'Programming Language',
            'last_used': 2023,
            'years_of_experience': 5.0,
            #'attractiveness': 3
        }
        response = client.post(url, data)
        if response.status_code != 302:
            print(f"Status Code: {response.status_code}")
            print(f"Response Content: {response.content.decode('utf-8')}")
        assert response.status_code == 302
        assert CompetencyModel.objects.count() == 1

    def test_list_competencies(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        mixer.cycle(3).blend(CompetencyModel, user=user)
        url = reverse('list_competencies')
        response = client.get(url)
        assert response.status_code == 200
        assert 'formset' in response.context
        formset = response.context['formset']
        assert formset.queryset.count() == 3

    def test_update_competency(self, client):
        user = mixer.blend(User)
        competency = mixer.blend(CompetencyModel, user=user)
        client.force_login(user)
        url = reverse('update_competency', kwargs={'competency_id': competency.competency_id})
        data = {
            'name': 'Updated Competency',
            'level': 4,
            'category': 'Updated Category',
            'last_used': 2022,
            'years_of_experience': 4.5,
            'attractiveness': 4
        }
        response = client.post(url, data)
        assert response.status_code == 302
        competency.refresh_from_db()
        assert competency.name == 'Updated Competency'

    def test_delete_competency(self, client):
        user = mixer.blend(User)
        competency = mixer.blend(CompetencyModel, user=user)
        client.force_login(user)
        url = reverse('delete_competency', kwargs={'competency_id': competency.competency_id})
        response = client.post(url)
        assert response.status_code == 302
        assert CompetencyModel.objects.count() == 0

    def test_build_competencies_from_content(self, client, competencies, job_positions):
        user = mixer.blend(User)
        client.force_login(user)
        cv_content_repository = CvContentRepository()
        cv_content_repository.create_job_positions(user, job_positions)
        cv_content_repository.create_competencies(user, competencies)
        url = reverse('build_competencies_from_content')
        response = client.get(url)
        assert response.status_code == 302
        assert CompetencyModel.objects.count() > 2
