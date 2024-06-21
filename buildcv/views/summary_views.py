from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from loguru import logger

from buildcv.forms import SummaryForm
from buildcv.models import JobPost, CvCreationProcess
from buildcv.services import GenerateSummaryService
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
