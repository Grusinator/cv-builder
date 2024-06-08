from django.contrib.auth.models import User
from django.db import models


class EducationModel(models.Model):
    education_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)


class JobPositionModel(models.Model):
    job_position_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_positions')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    competencies = models.JSONField(default=list)  # Storing list of strings in JSONField


class CompetencyModel(models.Model):
    competency_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competencies')
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    category = models.CharField(max_length=255, blank=True, null=True)
    last_used = models.IntegerField()
    years_of_experience = models.FloatField()
    attractiveness = models.IntegerField(default=0)

    @property
    def level_description(self):
        levels = {
            1: 'Some knowledge',
            2: 'Knowledgeable',
            3: 'Experienced',
            4: 'Highly experienced',
            5: 'Expert'
        }
        return levels.get(self.level, None)


class ProjectModel(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generic_projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    effort_in_years = models.FloatField()
    last_updated = models.DateField()
    competencies = models.JSONField()
    def __str__(self):
        return self.name

