from django.contrib import admin

# Register your models here.
from users.models.models import ProfileModel

admin.site.register(ProfileModel)
