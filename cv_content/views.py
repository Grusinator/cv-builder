from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import FileUploadForm
from .forms import JobPositionForm

from .models import JobPositionModel
from .services import CVBuilderService


@login_required
def update_job_position(request, job_id):
    job = get_object_or_404(JobPositionModel, job_position_id=job_id, user=request.user)
    if request.method == 'POST':
        form = JobPositionForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('list_job_positions')
    else:
        form = JobPositionForm(instance=job)
    return render(request, 'update_job_position.html', {'form': form})


@login_required
@require_POST  # Ensure that this view can only be accessed via POST request
def delete_job_position(request, job_id):
    job = JobPositionModel.objects.get(pk=job_id)
    job.delete()
    return redirect('list_job_positions')


@login_required
def list_job_positions(request):
    service = CVBuilderService()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            service = CVBuilderService()
            try:
                # Assuming your service class has a method to handle PDF bytes
                messages.info(request, 'Processing file... Please wait.')
                service.load_job_positions_from_pdf(request.user, pdf_file.read())
                messages.success(request, 'File successfully processed.')
                # Optionally redirect to a new URL:
                return redirect('list_job_positions')
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = FileUploadForm()

    # Assuming you have a method to get all job positions
    job_positions = service.repository.get_job_positions(user=request.user)
    return render(request, 'job_positions.html', {'form': form, 'job_positions': job_positions})


@login_required
def add_job_position(request):
    if request.method == 'POST':
        form = JobPositionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('list_job_positions')  # Redirect to a new URL
    else:
        form = JobPositionForm(user=request.user)
    return render(request, 'add_job_position.html', {'form': form})


def show_content(request):
    return render(request, 'cv_content_base.html')
