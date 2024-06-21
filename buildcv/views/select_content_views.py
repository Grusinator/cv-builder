from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from loguru import logger
from django.contrib import messages

from buildcv.forms import CvContentForm
from buildcv.models import JobPost, CvCreationProcess
from buildcv.services import FilterRelevantContentService

@login_required
def manage_content_selection(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation, created = CvCreationProcess.objects.get_or_create(user=request.user, job_post=job_post)

    if request.method == 'POST':
        logger.debug('POST data: %s', request.POST)
        if 'select_relevant_content' in request.POST:
            logger.debug('Select relevant content button pressed.')
            form = CvContentForm(request.POST, instance=cv_creation, user=request.user)
            if form.is_valid():
                num_projects = form.cleaned_data.get('num_projects', 3)
                num_competencies = form.cleaned_data.get('num_competencies', 10)
                service = FilterRelevantContentService()
                matching_competencies = service.find_most_relevant_competencies(job_post, n=num_competencies)
                matching_projects = service.find_most_relevant_projects(job_post, n=num_projects)
                logger.debug(f'Matching competencies: {matching_competencies}')
                logger.debug(f'Matching projects: {matching_projects}')
                initial_competency_ids = [comp.competency_id for comp in matching_competencies]
                initial_project_ids = [proj.project_id for proj in matching_projects]

                form = CvContentForm(instance=cv_creation, user=request.user,
                                     initial_competency_ids=initial_competency_ids,
                                     initial_project_ids=initial_project_ids)
            else:
                msg = f'Error in form: {form.errors}'
                logger.error(msg)
                messages.error(request, msg)
        elif 'save_content' in request.POST:
            form = CvContentForm(request.POST, instance=cv_creation, user=request.user)
            if form.is_valid():
                logger.debug('Form is valid. Saving form.')
                form.save()
                return redirect('create_cv', job_post_id=job_post_id)
            else:
                msg = f'Error saving form: {form.errors}'
                logger.error(msg)
                messages.error(request, msg)
    else:
        form = CvContentForm(instance=cv_creation, user=request.user)
        logger.debug('GET request. Form initialized with instance and initial data.')

    logger.debug('Rendering manage_content_selection.html with form: %s', form)
    return render(request, 'manage_content_selection.html', {'job_post': job_post, 'form': form})
