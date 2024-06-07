from django.contrib import admin

from .models import JobPositionModel, EducationModel, ProjectModel, CompetencyModel

admin.site.register(JobPositionModel)
admin.site.register(EducationModel)
admin.site.register(ProjectModel)
admin.site.register(CompetencyModel)
