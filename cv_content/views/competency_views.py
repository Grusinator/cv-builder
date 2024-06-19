from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from loguru import logger

from cv_content.forms import CompetencyForm
from cv_content.forms.competency_forms import CompetencyFormSet
from cv_content.models import CompetencyModel
from cv_content.services import CVContentCreaterService


@login_required
def build_competencies_from_content(request):
    service = CVContentCreaterService()
    user = request.user
    try:
        service.build_competencies_from_projects_and_jobs(user)
        messages.success(request, 'Competencies successfully analyzed and created.')
    except Exception as e:
        msg = f'Error fetching competencies'
        logger.exception(msg, exc_info=True)
        messages.error(request, msg)
    return redirect('list_competencies')


@login_required
def add_competency(request):
    if request.method == 'POST':
        form = CompetencyForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_competencies')
        else:
            messages.error(request, f"Error adding competency.: {form.errors}")
    else:
        form = CompetencyForm(user=request.user)
    return render(request, 'upsert_with_form.html', {'form': form})


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
    return render(request, 'upsert_with_form.html', {'form': form})


@login_required
@require_POST
def delete_competency(request, competency_id):
    service = CVContentCreaterService()
    try:
        logger.debug(f"Deleting competency with id: {competency_id}")
        service.repository.delete_competency(user=request.user, competency_id=competency_id)
    except Exception as e:
        logger.exception(f"Error deleting competency: {str(e)}")
        raise Http404(f'Error deleting competency: {str(e)}')

    return redirect('list_competencies')


@login_required
def list_competencies(request):
    competencies = CompetencyModel.objects.filter(user=request.user)

    # Round years_of_experience to 1 decimal place for display
    for competency in competencies:
        competency.years_of_experience = round(competency.years_of_experience, 1)

    if request.method == 'POST':
        logger.debug(f"POST data: {request.POST}")
        formset = CompetencyFormSet(request.POST, queryset=competencies)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.years_of_experience = round(instance.years_of_experience, 1)
                logger.debug(f"Saving instance with id: {instance.competency_id}")
                instance.save()
            formset.save_m2m()
            messages.success(request, "Competencies updated successfully.")
            logger.debug("Formset saved successfully.")
            return redirect('list_competencies')
        else:
            for form in formset:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                        logger.error(f"Form errors: {form.errors}")
    else:
        formset = CompetencyFormSet(queryset=competencies)

    return render(request, 'list_competencies.html', {'formset': formset})
