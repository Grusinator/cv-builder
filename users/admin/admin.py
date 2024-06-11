from django.contrib import admin

# Register your models here.
from users.models.profile import ProfileModel

admin.site.register(ProfileModel)
