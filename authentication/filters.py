from django_filters import rest_framework as filters
from .models import Client


class ClientFilter(filters.FilterSet):
    class Meta:
        model = Client
        fields = {
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains']
        }
