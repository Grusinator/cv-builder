from django.contrib import admin

from dataproviders.models import DataProvider, Endpoint, OauthConfig, HttpConfig, \
    DataProviderUser
from dataproviders.services import oauth

models = (
    OauthConfig,
    HttpConfig,
)

[admin.site.register(model) for model in models]


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['endpoint_name']
    model = Endpoint



@admin.register(DataProvider)
class DataProviderAdmin(admin.ModelAdmin):
    # list_display = ['profile', 'provider.provider_name']
    ordering = ['provider_name']


@admin.register(DataProviderUser)
class DataProviderUserAdmin(admin.ModelAdmin):
    # list_display = ['profile__user__username', 'provider__provider_name']
    # ordering = ['profile']
    actions = [
        "refresh_token",
    ]

    def refresh_token(self, request, queryset):
        for data_provider_user in queryset:
            oauth.refresh_access_token(data_provider_user)
