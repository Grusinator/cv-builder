from allauth.socialaccount.models import SocialToken
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from loguru import logger

from cv_content.forms import ProjectForm
from cv_content.models import ProjectModel
from cv_content.services import CVContentCreaterService


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_projects')
    else:
        form = ProjectForm(user=request.user)
    return render(request, 'upsert_with_form.html', {'form': form})


@login_required
def update_project(request, project_id):
    project = get_object_or_404(ProjectModel, project_id=project_id, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'upsert_with_form.html', {'form': form, 'title': 'Update Project'})


@login_required
@require_POST
def delete_project(request, project_id):
    project = ProjectModel.objects.get(pk=project_id, user=request.user)
    project.delete()
    return redirect('list_projects')


@login_required
def list_projects(request):
    service = CVContentCreaterService()
    projects = service.repository.get_projects(user=request.user)
    return render(request, 'list_projects.html', {'projects': projects})


@login_required
def fetch_github_projects(request):
    try:
        if request.user.is_authenticated:
            github_account = request.user.socialaccount_set.filter(provider='github').first()
            logger.debug(f'github_account: {github_account}')
            if github_account:
                service = CVContentCreaterService()
                github_token = SocialToken.objects.get(account=github_account)
                service.fetch_github_projects(request.user, github_token)
                messages.success(request, 'Projects fetched successfully from GitHub.')
            else:
                messages.error(request, 'GitHub account not connected.')

        return redirect('list_projects')
    except Exception as e:
        logger.exception(f'Error fetching projects from GitHub', exc_info=True)
        messages.error(request, f'Error fetching projects from GitHub error')
    return redirect('list_projects')
