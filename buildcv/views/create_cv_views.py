from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from loguru import logger

from buildcv.forms import CvTemplateForm
from buildcv.models import JobPost, CvCreationProcess
from buildcv.repositories.cv_creation_repository import CvCreationRepository
from buildcv.services import BuildLatexCVService


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
