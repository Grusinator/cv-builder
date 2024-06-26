# Generated by Django 5.0.6 on 2024-06-08 19:22

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("buildcv", "0002_remove_educationmodel_user_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="JobPost",
            fields=[
                ("job_post_id", models.AutoField(primary_key=True, serialize=False)),
                ("company_name", models.CharField(max_length=255)),
                ("job_title", models.CharField(max_length=255)),
                ("job_post_text", models.TextField()),
                (
                    "recruiter_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CvCreationProcess",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("summary", models.TextField(blank=True, null=True)),
                ("projects", models.JSONField(blank=True, default=list, null=True)),
                ("competencies", models.JSONField(blank=True, default=list, null=True)),
                (
                    "job_positions",
                    models.JSONField(blank=True, default=list, null=True),
                ),
                ("educations", models.JSONField(blank=True, default=list, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "cv_file",
                    models.FileField(blank=True, null=True, upload_to="cv_files/"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cv_creation_processes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "job_post",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cv_creation_processes",
                        to="buildcv.jobpost",
                    ),
                ),
            ],
        ),
    ]
