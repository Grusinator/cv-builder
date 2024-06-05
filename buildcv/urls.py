from django.urls import path

from . import views

app_name = 'buildcv'
urlpatterns = [
    path('buildcv/', views.buildcv, name='buildcv'),
    path('', views.home_view, name="home"),
]