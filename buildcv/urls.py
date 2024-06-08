from django.urls import path
from .views import list_job_posts, add_job_post, update_job_post, delete_job_post, build_cv_panel, home_view, \
    create_cv, generate_summary

urlpatterns = [
    path('', home_view, name='buildcv'),
    path('job_posts/', list_job_posts, name='list_job_posts'),
    path('job_post/add/', add_job_post, name='add_job_post'),
    path('job_post/update/<int:job_post_id>/', update_job_post, name='update_job_post'),
    path('job_post/delete/<int:job_post_id>/', delete_job_post, name='delete_job_post'),

    path('job-post/create-cv/<int:job_post_id>/', create_cv, name='create_cv'),
    path('job-post/generate-summary/', generate_summary, name='generate_summary'),

    path('panel/', build_cv_panel, name='buildcv'),

]
