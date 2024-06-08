from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from loguru import logger

from buildcv.forms.cv_creation_form import CvCreationForm
from buildcv.models import JobPost
from cv_content.models import ProjectModel, CompetencyModel, EducationModel

from django.http import JsonResponse

from cv_content.services import CVContentCreaterService


@login_required
def create_cv(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    projects = ProjectModel.objects.filter(user=request.user)
    competencies = CompetencyModel.objects.filter(user=request.user)
    educations = EducationModel.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CvCreationForm(request.POST, user=request.user)
        if form.is_valid():
            cv_process = form.save(commit=False)
            cv_process.user = request.user
            cv_process.job_post = job_post
            cv_process.save()
            # Here you would call the service to create the CV PDF
            messages.success(request, 'CV created successfully.')
            return redirect('list_job_posts')
    else:
        form = CvCreationForm(user=request.user)

    return render(request, 'create_cv.html', {
        'form': form,
        'job_post': job_post,
        'projects': projects,
        'competencies': competencies,
        'educations': educations
    })



@login_required
def generate_summary(request):
    if request.method == 'POST':
        job_post_id = request.POST.get('job_post_id')
        job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
        projects = ProjectModel.objects.filter(user=request.user)
        competencies = CompetencyModel.objects.filter(user=request.user)
        educations = EducationModel.objects.filter(user=request.user)

        CVContentCreaterService()
        try:
            summary = your_service_function(job_post, projects, competencies, educations)
        except Exception as e:
            logger.exception(f'Error generating summary')
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'summary': summary})
