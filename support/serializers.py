from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    client_first_name = serializers.CharField(read_only=True, source='client.first_name')
    client_last_name = serializers.CharField(read_only=True, source='client.last_name')
    client_email = serializers.CharField(read_only=True, source='client.email')
    support_contact = serializers.CharField(read_only=True, source='client.sales_contact')
    support_contact_first_name = serializers.CharField(read_only=True, source='support_contact.first_name')
    support_contact_last_name = serializers.CharField(read_only=True, source='support_contact.last_name')
    support_contact_email = serializers.CharField(read_only=True, source='support_contact.email')

    class Meta:
        model = Event
        fields = ['id', 'client', 'client_first_name', 'client_last_name', 'client_email', 'date_created', 'date_updated', 'status', 'attendees', 'event_date', 'notes', 'support_contact', 'support_contact_first_name', 'support_contact_last_name', 'support_contact_email']
