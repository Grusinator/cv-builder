from django.urls import path

from . import views

app_name = 'buildcv'
urlpatterns = [
    path('', views.buildcv, name='buildcv'),
]