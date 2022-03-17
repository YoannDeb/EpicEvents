from django_filters import rest_framework as filters
from .models import Contract


class ContractFilter(filters.FilterSet):
    """
    Contract filter for API search.
    """
    class Meta:
        model = Contract
        fields = {
            'client__last_name': ['exact', 'icontains'],
            'client__email': ['exact', 'icontains'],
            'date_created': ['exact', 'icontains', 'gte', 'lte'],
            'amount': ['exact', 'gte', 'lte']
        }
