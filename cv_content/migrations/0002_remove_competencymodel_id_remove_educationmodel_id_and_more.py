# Generated by Django 5.0.6 on 2024-06-07 12:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cv_content", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="competencymodel",
            name="id",
        ),
        migrations.RemoveField(
            model_name="educationmodel",
            name="id",
        ),
        migrations.RemoveField(
            model_name="jobpositionmodel",
            name="id",
        ),
        migrations.RemoveField(
            model_name="projectmodel",
            name="id",
        ),
        migrations.AddField(
            model_name="competencymodel",
            name="competency_id",
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="educationmodel",
            name="education_id",
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="jobpositionmodel",
            name="job_position_id",
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="projectmodel",
            name="project_id",
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
