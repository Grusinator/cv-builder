from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from cv_content.forms import CompetencyForm
from cv_content.models import CompetencyModel
from cv_content.services import CVBuilderService

@login_required
def fetch_competencies(request):
    service = CVBuilderService()
    user = request.user
    try:
        competencies = service.build_competencies_from_projects_and_jobs(user)
        messages.success(request, 'Competencies successfully analyzed and created.')
    except Exception as e:
        messages.error(request, f'Error fetching competencies: {str(e)}')
    return redirect('list_competencies')

@login_required
def add_competency(request):
    if request.method == 'POST':
        form = CompetencyForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_competencies')
    else:
        form = CompetencyForm(user=request.user)
    return render(request, 'add_competency.html', {'form': form})

@login_required
def update_competency(request, competency_id):
    competency = get_object_or_404(CompetencyModel, competency_id=competency_id, user=request.user)
    if request.method == 'POST':
        form = CompetencyForm(request.POST, instance=competency, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_competencies')
    else:
        form = CompetencyForm(instance=competency)
    return render(request, 'update_competency.html', {'form': form})

@login_required
@require_POST
def delete_competency(request, competency_id):
    service = CVBuilderService()
    try:
        service.repository.delete_competency(user=request.user, competency_id=competency_id)
    except Exception as e:
        raise Http404(f'Error deleting competency: {str(e)}')

    return redirect('list_competencies')

@login_required
def list_competencies(request):
    service = CVBuilderService()
    competencies = service.repository.get_competencies(user=request.user)
    return render(request, 'list_competencies.html', {'competencies': competencies})
