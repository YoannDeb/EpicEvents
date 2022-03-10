from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'client__last_name': ['exact', 'icontains'],
            'client__email': ['exact', 'icontains'],
            'event_date': ['exact', 'gte', 'lte']
        }
