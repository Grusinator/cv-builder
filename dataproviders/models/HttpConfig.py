from collections import OrderedDict

from django.db import models


import json
from dataproviders.models import DataProvider


class HttpConfig(models.Model):

    data_provider = models.OneToOneField(DataProvider, related_name="http_config", on_delete=models.CASCADE)
    header = models.JSONField(null=True, blank=True)
    url_encoded_params = models.JSONField(null=True, blank=True)
    body_type = models.TextField(null=True, blank=True)
    body_content = models.TextField(null=True, blank=True)
    request_type = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"HTTP Config:{self.data_provider.provider_name}"

    def build_header(self):
        try:
            return dict(json.loads(self.header))
        except Exception as e:
            return dict()
