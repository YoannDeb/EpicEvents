from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'support_contact', 'client', 'date_created', 'date_updated', 'status', 'attendees', 'event_date', 'notes']
