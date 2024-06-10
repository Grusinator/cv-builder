"""cvbuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from bokeh_django import autoload, static_extensions
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

import cv_app

pn_app_config = apps.get_app_config('bokeh_django')

urlpatterns = [
    path('buildcv/', include('buildcv.urls')),
    path("", include("core.urls")),
    path('users/', include('users.urls')),
    path("cv_content/", include("cv_content.urls")),
    path('admin/', admin.site.urls),
]

bokeh_apps = [
    autoload("buildcv", cv_app.app),
]

urlpatterns += static_extensions()
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
