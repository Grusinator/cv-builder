from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from loguru import logger

from buildcv.forms import SummaryForm, CvContentForm
from buildcv.models import JobPost, CvCreationProcess
from buildcv.repositories.cv_creation_repository import CvCreationRepository
from buildcv.services import BuildLatexCVService
from buildcv.services.filter_relevant_content_service import FilterRelevantContentService
from buildcv.services.generate_summary_service import GenerateSummaryService
from cv_content.models import ProjectModel, CompetencyModel, EducationModel
from cv_content.repositories import CvContentRepository
from users.models import ProfileModel


@login_required
@require_POST
def generate_summary(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation, created = CvCreationProcess.objects.get_or_create(user=request.user, job_post=job_post)

    projects = ProjectModel.objects.filter(user=request.user)
    competencies = CompetencyModel.objects.filter(user=request.user)
    educations = EducationModel.objects.filter(user=request.user)

    try:
        summary = GenerateSummaryService().generate_summary_from_llm(job_post, projects, competencies, educations)
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
            messages.success(request, 'Summary saved successfully.')
            return redirect('manage_content_selection', job_post_id=job_post.job_post_id)
    else:
        form = SummaryForm(instance=cv_creation)

    return render(request, 'manage_summary.html', {'form': form, 'job_post': job_post})


@login_required
def manage_content_selection(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation, created = CvCreationProcess.objects.get_or_create(user=request.user, job_post=job_post)

    if request.method == 'POST':
        form = CvContentForm(request.POST, instance=cv_creation, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('create_cv', job_post_id=job_post_id)
        else:
            logger.error(f'Error saving form: {form.errors}')
    else:
        form = CvContentForm(instance=cv_creation, user=request.user)  # Pass user here
        service = FilterRelevantContentService()
        competencies = CvContentRepository().get_competencies(user=request.user)
        matching_competencies = service.find_most_relevant_competencies_to_job_add(job_post.job_post_text, competencies)
        form.fields['competencies'].initial = [comp.competency_id for comp in matching_competencies]

    return render(request, 'manage_content_selection.html', {'job_post': job_post, 'form': form})


@login_required
def create_cv(request, job_post_id):
    job_post: JobPost = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    cv_creation: CvCreationProcess = get_object_or_404(CvCreationProcess, user=request.user, job_post=job_post)
    if request.method == 'POST':
        logger.debug('Creating CV')
        repository = CvCreationRepository()
        cv_service = BuildLatexCVService()
        cv_creation_content = repository.get_cv_creation_content(user=request.user, job_post=job_post)
        media = repository.get_media(user=request.user)

        pdf_file = cv_service.build_cv_from_content(cv_creation_content, media_content=media)
        cv_file_content = ContentFile(pdf_file)
        cv_creation.cv_file.save(f'{job_post.job_title}.pdf', cv_file_content)
        messages.success(request, 'CV created successfully.')

    return render(request, 'create_cv.html',
                  {'job_post': job_post, 'cv_creation': cv_creation,
                   'pdf_path': cv_creation.cv_file.url if cv_creation.cv_file else None})
