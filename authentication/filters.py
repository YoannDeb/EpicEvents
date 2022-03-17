from django_filters import rest_framework as filters
from .models import Client


class ClientFilter(filters.FilterSet):
    """
    Client filter for API search.
    """
    class Meta:
        model = Client
        fields = {
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains']
        }
