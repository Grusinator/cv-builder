from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cv_content.forms import FileUploadForm
from cv_content.forms.education import EducationForm
from cv_content.models import EducationModel
from cv_content.services import CVContentCreaterService

CVContentCreaterService = CVContentCreaterService

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_educations')
    else:
        form = EducationForm(user=request.user)
    return render(request, 'upsert_with_form.html', {'form': form})


@login_required
def update_education(request, education_id):
    education = get_object_or_404(EducationModel, education_id=education_id, user=request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_educations')
    else:
        form = EducationForm(instance=education)
    return render(request, 'upsert_with_form.html', {'form': form})


@login_required
@require_POST
def delete_education(request, education_id):
    service = CVContentCreaterService()
    try:
        service.repository.delete_education(user=request.user, education_id=education_id)
    except Exception as e:
        raise Http404(f'Error deleting education: {str(e)}')

    return redirect('list_educations')


@login_required
def list_educations(request):
    service = CVContentCreaterService()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            service = CVContentCreaterService()
            try:
                # Assuming your service class has a method to handle PDF bytes
                messages.info(request, 'Processing file... Please wait.')
                service.load_educations_from_pdf(request.user, pdf_file.read())
                messages.success(request, 'File successfully processed.')
                # Optionally redirect to a new URL:
                return redirect('list_educations')
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = FileUploadForm()

    # Assuming you have a method to get all job positions
    educations = service.repository.get_educations(user=request.user)
    return render(request, 'list_educations.html', {'form': form, 'educations': educations})
