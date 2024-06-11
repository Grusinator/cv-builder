
from django.contrib.auth import logout, login
from django.urls import include
from django.urls import path

from users.views import signup_view
from .views import manage_profile

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', manage_profile, name='manage_profile'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout, {'next_page': '/login/'}, name='logout'),
    path('login/', login, {'next_page': '/'}, name='login'),
]
