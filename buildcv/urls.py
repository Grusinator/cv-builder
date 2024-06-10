from django.urls import path
from .views import list_job_posts, add_job_post, update_job_post, delete_job_post, build_cv_panel, home_view, \
    manage_summary, generate_summary, manage_content_selection, create_cv

urlpatterns = [
    path('', home_view, name='buildcv'),
    path('job_posts/', list_job_posts, name='list_job_posts'),
    path('job_post/add/', add_job_post, name='add_job_post'),
    path('job_post/update/<int:job_post_id>/', update_job_post, name='update_job_post'),
    path('job_post/delete/<int:job_post_id>/', delete_job_post, name='delete_job_post'),

    path('job_post/<int:job_post_id>/generate_summary/', generate_summary, name='generate_summary'),
    path('job_post/<int:job_post_id>/manage_summary/', manage_summary, name='manage_summary'),

    path('cv/<int:job_post_id>/content/', manage_content_selection, name='manage_content_selection'),
    path('cv/<int:job_post_id>/generate/', create_cv, name='create_cv'),

    path('panel/', build_cv_panel, name='buildcv'),

]
