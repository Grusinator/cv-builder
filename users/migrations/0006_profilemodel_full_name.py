# Generated by Django 5.0.6 on 2024-06-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_remove_profilemodel_id_profilemodel_profile_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="profilemodel",
            name="full_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
