import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from cv_content.models import ProjectModel

@pytest.mark.django_db
class TestProjectViews:
    def test_add_project(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        url = reverse('add_project')
        data = {
            'name': 'New Project',
            'description': 'Project Description',
            'effort_in_years': 1.5,
            'competencies': '["Python", "Django"]'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert ProjectModel.objects.count() == 1

    def test_list_projects(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        mixer.cycle(3).blend(ProjectModel, user=user, competencies=['Python'], description='Project Description')
        url = reverse('list_projects')
        response = client.get(url)
        assert response.status_code == 200
        assert 'projects' in response.context
        assert len(response.context['projects']) == 3

    def test_update_project(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        project = mixer.blend(ProjectModel, user=user, competencies=['Python'])
        url = reverse('update_project', kwargs={'project_id': project.project_id})
        data = {
            'name': 'Updated Project',
            'description': 'Updated Description',
            'effort_in_years': 2.0,
            'competencies': '["Java", "Spring"]'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        project.refresh_from_db()
        assert project.name == 'Updated Project'
        assert project.description == 'Updated Description'

    def test_delete_project(self, client):
        user = mixer.blend(User)
        client.force_login(user)
        project = mixer.blend(ProjectModel, user=user, competencies=['Python'])
        url = reverse('delete_project', kwargs={'project_id': project.project_id})
        response = client.post(url)
        assert response.status_code == 302
        assert ProjectModel.objects.count() == 0

    def test_fetch_github_projects(self, client, mocker):
        user = mixer.blend(User)
        client.force_login(user)
        mock_service = mocker.patch('cv_content.services.CVBuilderService.fetch_github_projects', return_value=None)
        url = reverse('fetch_github_projects')
        data = {'github_username': 'testuser', 'github_token': 'testtoken'}
        response = client.post(url, data)
        assert response.status_code == 302
        mock_service.assert_called_once_with(user, 'testuser', 'testtoken')

