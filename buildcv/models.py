from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class JobPost(models.Model):
    job_post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_post_text = models.TextField()
    recruiter_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class CvCreationProcess(models.Model):
    job_post = models.OneToOneField(JobPost, on_delete=models.CASCADE, related_name='cv_creation_processes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cv_creation_processes')
    summary = models.TextField(null=True, blank=True)
    projects = models.JSONField(default=list, null=True, blank=True)
    competencies = models.JSONField(default=list, null=True, blank=True)
    job_positions = models.JSONField(default=list, null=True, blank=True)
    educations = models.JSONField(default=list, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    cv_file = models.FileField(upload_to='cv_files/', null=True, blank=True)

    def __str__(self):
        return f"CV Process for {self.user.username} created on {self.created_at}"
