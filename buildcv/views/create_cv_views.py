from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from loguru import logger

from buildcv.forms import SummaryForm, CvContentForm, CvTemplateForm
from buildcv.models import JobPost, CvCreationProcess
from buildcv.repositories.cv_creation_repository import CvCreationRepository
from buildcv.services import BuildLatexCVService
from buildcv.services.filter_relevant_content_service import FilterRelevantContentService
from buildcv.services.generate_summary_service import GenerateSummaryService
from cv_content.models import ProjectModel, CompetencyModel, EducationModel


@login_required
@require_POST
def generate_summary(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation, created = CvCreationProcess.objects.get_or_create(user=request.user, job_post=job_post)

    projects = ProjectModel.objects.filter(user=request.user)
    competencies = CompetencyModel.objects.filter(user=request.user)
    educations = EducationModel.objects.filter(user=request.user)

    try:
        profile_description = request.user.profile.profile_description
        guidance = cv_creation.summary_guidance
        service = GenerateSummaryService()
        summary = service.generate_summary_from_llm(guidance, job_post, projects, competencies, educations,
                                                    profile_description)
        cv_creation.summary = summary
        cv_creation.save()
        messages.success(request, 'Summary generated successfully.')
    except Exception as e:
        logger.exception(f'Error generating summary')
        messages.error(request, f'Error generating summary: {str(e)}')

    return redirect('manage_summary', job_post_id=job_post.job_post_id)


@login_required
def manage_summary(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation, created = CvCreationProcess.objects.get_or_create(user=request.user, job_post=job_post)

    if request.method == 'POST':
        form = SummaryForm(request.POST, instance=cv_creation)
        if form.is_valid():
            form.save()
            if 'generate_summary_btn' in request.POST:
                # Generate summary
                projects = ProjectModel.objects.filter(user=request.user)
                competencies = CompetencyModel.objects.filter(user=request.user)
                educations = EducationModel.objects.filter(user=request.user)
                try:
                    profile_description = request.user.profile.profile_description
                    guidance = cv_creation.summary_guidance
                    service = GenerateSummaryService()
                    summary = service.generate_summary_from_llm(guidance, job_post, projects, competencies, educations,
                                                                profile_description)
                    cv_creation.summary = summary
                    cv_creation.save()
                    messages.success(request, 'Summary generated successfully.')
                except Exception as e:
                    logger.exception('Error generating summary')
                    messages.error(request, f'Error generating summary: {str(e)}')
            else:
                messages.success(request, 'Summary saved successfully.')
            return redirect('manage_summary', job_post_id=job_post.job_post_id)
    else:
        form = SummaryForm(instance=cv_creation)

    return render(request, 'manage_summary.html', {'form': form, 'job_post': job_post})


@login_required
def manage_content_selection(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation, created = CvCreationProcess.objects.get_or_create(user=request.user, job_post=job_post)

    initial_competency_ids = [436, 437, 442, 449, 495]
    initial_project_ids = []

    if request.method == 'POST':
        logger.debug('POST data: %s', request.POST)
        if 'select_relevant_content' in request.POST:
            logger.debug('Select relevant content button pressed.')
            service = FilterRelevantContentService()
            matching_competencies = service.find_most_relevant_competencies(job_post)
            matching_projects = service.find_most_relevant_projects(job_post)
            logger.debug(f'Matching competencies: {matching_competencies}')
            logger.debug(f'Matching projects: {matching_projects}')

            # Set initial values for competencies and projects
            initial_competency_ids = [comp.competency_id for comp in matching_competencies]
            initial_project_ids = [proj.project_id for proj in matching_projects]

            form = CvContentForm(request.POST, instance=cv_creation, user=request.user,
                                 initial_competency_ids=initial_competency_ids,
                                 initial_project_ids=initial_project_ids)
        else:
            form = CvContentForm(request.POST, instance=cv_creation, user=request.user)

            if 'save_content' in request.POST:
                if form.is_valid():
                    logger.debug('Form is valid. Saving form.')
                    form.save()
                    return redirect('create_cv', job_post_id=job_post_id)
                else:
                    logger.error(f'Error saving form: {form.errors}')
    else:
        form = CvContentForm(instance=cv_creation, user=request.user,
                             initial_competency_ids=initial_competency_ids,
                             initial_project_ids=initial_project_ids)
        logger.debug('GET request. Form initialized with instance and initial data.')

    logger.debug('Rendering manage_content_selection.html with form: %s', form)
    return render(request, 'manage_content_selection.html', {'job_post': job_post, 'form': form})


@login_required
def create_cv(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation = get_object_or_404(CvCreationProcess, user=request.user, job_post=job_post)
    template_form = CvTemplateForm(request.POST or None)

    if request.method == 'POST' and template_form.is_valid():
        logger.debug('Creating CV')
        repository = CvCreationRepository()
        cv_service = BuildLatexCVService()
        cv_creation_content = repository.get_cv_creation_content(user=request.user, job_post=job_post)
        media = repository.get_media(user=request.user)

        template = template_form.cleaned_data['template']
        pdf_file = cv_service.build_cv_from_content(cv_creation_content,
                                                    template_file=Path(template.template_file.path),
                                                    media_content=media)
        cv_file_content = ContentFile(pdf_file)
        cv_creation.cv_file.save(f'{job_post.job_title}.pdf', cv_file_content)
        messages.success(request, 'CV created successfully.')

    return render(request, 'create_cv.html',
                  {'job_post': job_post, 'cv_creation': cv_creation, 'template_form': template_form,
                   'pdf_path': cv_creation.cv_file.url if cv_creation.cv_file else None})
