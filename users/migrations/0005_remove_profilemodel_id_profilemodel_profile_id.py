# Generated by Django 5.0.6 on 2024-06-08 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_profilemodel_delete_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profilemodel",
            name="id",
        ),
        migrations.AddField(
            model_name="profilemodel",
            name="profile_id",
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]