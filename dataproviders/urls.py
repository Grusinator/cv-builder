
from django.urls import path

from dataproviders.views import *

urlpatterns = [
    path('', data_provider_list_view, name='providers'),
    path(r'oauth2redirect/', oauth2redirect_view, name='oauth2redirect'),
    path('<str:provider_name>/', data_provider_view, name='provider_detail'),
    path('<str:provider_name>/endpoint/<str:endpoint_name>/', endpoint_detail_view, name='endpoint_detail'),
]
