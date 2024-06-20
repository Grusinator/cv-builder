from django.contrib import admin

# Register your models here.
from .models import JobPost, CvCreationProcess, CvTemplate

admin.site.register(JobPost)
admin.site.register(CvCreationProcess)
admin.site.register(CvTemplate)
