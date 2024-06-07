from django.urls import path

from .views import list_job_positions, add_job_position, update_job_position, show_content, delete_job_position
from .views import add_education, update_education, delete_education, list_educations

from cv_content.views import add_project, update_project, delete_project, list_projects, fetch_github_projects

from django.urls import path
from .views import add_competency, update_competency, delete_competency, list_competencies, fetch_competencies

urlpatterns = [
    path('competencies/', list_competencies, name='list_competencies'),
    path('competency/add/', add_competency, name='add_competency'),
    path('competency/update/<int:competency_id>/', update_competency, name='update_competency'),
    path('competency/delete/<int:competency_id>/', delete_competency, name='delete_competency'),
    path('competencies/fetch/', fetch_competencies, name='fetch_competencies'),

    path('projects/', list_projects, name='list_projects'),
    path('projects/add/', add_project, name='add_project'),
    path('projects/update/<int:project_id>/', update_project, name='update_project'),
    path('projects/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('projects/fetch/', fetch_github_projects, name='fetch_github_projects'),
    path("", show_content, name="show_content"),
    path('add-job/', add_job_position, name='add_job_position'),
    path('jobs/', list_job_positions, name='list_job_positions'),
    path('job/update/<int:job_id>/', update_job_position, name='update_job_position'),
    path('job/delete/<int:job_id>/', delete_job_position, name='delete_job_position'),


    path('education/add/', add_education, name='add_education'),
    path('education/update/<int:education_id>/', update_education, name='update_education'),
    path('education/delete/<int:education_id>/', delete_education, name='delete_education'),
    path('educations/', list_educations, name='list_educations'),
]


