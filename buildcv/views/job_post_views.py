from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from buildcv.forms import JobPostForm
from buildcv.models import JobPost


@login_required
def list_job_posts(request):
    job_posts = JobPost.objects.filter(user=request.user).order_by('state', '-deadline')
    now = timezone.now()
    return render(request, 'list_job_posts.html', {'job_posts': job_posts, 'now': now})


@login_required
def add_job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.user = request.user
            job_post.save()
            messages.success(request, 'Job post created successfully.')
            return redirect('list_job_posts')
    else:
        form = JobPostForm()
    return render(request, 'upsert_with_form.html', {'form': form, 'title': 'Add Job Post'})


@login_required
def update_job_post(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post updated successfully.')
            return redirect('list_job_posts')
    else:
        form = JobPostForm(instance=job_post)
    return render(request, 'upsert_with_form.html', {'form': form})


@require_POST
@login_required
def delete_job_post(request, job_post_id):
    job_post = get_object_or_404(JobPost, job_post_id=job_post_id, user=request.user)
    if request.method == 'POST':
        job_post.delete()
        messages.success(request, 'Job post deleted successfully.')
        return redirect('list_job_posts')
