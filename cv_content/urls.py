from django.urls import path

from .views import list_job_positions, add_job_position, update_job_position, show_content, delete_job_position

urlpatterns = [
    path("", show_content, name="show_content"),
    path('add-job/', add_job_position, name='add_job_position'),
    path('jobs/', list_job_positions, name='list_job_positions'),
    path('job/update/<int:job_id>/', update_job_position, name='update_job_position'),
    path('job/delete/<int:job_id>/', delete_job_position, name='delete_job_position'),
]
