from django.contrib.auth.models import User
from django.db import models


class ProfileModel(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        app_label = 'users'
        default_related_name = 'profile'

    @classmethod
    def model_validate(cls, obj):
        return Profile(
            **obj.__dict__,
            profile_picture=obj.profile_picture.url if obj.profile_picture else None
        )
