
from django.contrib.auth import logout, login
from django.urls import path, include

from users.views import signup_view

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),
    path('login/', login, {'next_page': '/'}, name='login'),
]
