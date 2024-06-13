from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse


class DataProvider(models.Model):
    icon_image_url = models.URLField(null=True, blank=True)
    # icon_image = models.ImageField(null=True, blank=True)
    provider_name = models.CharField(unique=True, max_length=50)
    provider_url = models.URLField(null=True, blank=True)
    api_endpoint = models.CharField(null=True, blank=True, max_length=255)

    def get_internal_view_url(self):
        return reverse('provider_detail', args=[str(self.provider_name)])

    def __str__(self):
        return "%s - %s" % (self.provider_name, self.api_endpoint)

    @classmethod
    def exists(cls, provider_name):
        try:
            return cls.objects.get(provider_name=provider_name)
        except ObjectDoesNotExist:
            return None

    class Meta:
        app_label = 'dataproviders'
