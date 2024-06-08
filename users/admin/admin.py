from django.contrib import admin

# Register your models here.
from users.models.profilemodel import ProfileModel

admin.site.register(ProfileModel)
