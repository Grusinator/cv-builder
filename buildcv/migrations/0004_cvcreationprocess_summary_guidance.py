# Generated by Django 5.0.6 on 2024-06-16 07:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("buildcv", "0003_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cvcreationprocess",
            name="summary_guidance",
            field=models.TextField(blank=True, null=True),
        ),
    ]
