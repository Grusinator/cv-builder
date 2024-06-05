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
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

import cv_app
from ui.panel.app import CVBuilderApp

pn_app_config = apps.get_app_config('bokeh_django')

urlpatterns = [
    path('', include('buildcv.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]


def app(doc):
    """This function is necessary for the app to be served by Django."""
    app = CVBuilderApp().view()
    app.server_doc(doc)


bokeh_apps = [
    autoload("buildcv", cv_app.app),
]

urlpatterns += static_extensions()
urlpatterns += staticfiles_urlpatterns()
