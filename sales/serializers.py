from rest_framework import serializers

from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    client_first_name = serializers.CharField(read_only=True, source='client.first_name')
    client_last_name = serializers.CharField(read_only=True, source='client.last_name')
    client_email = serializers.CharField(read_only=True, source='client.email')
    sales_contact = serializers.IntegerField(read_only=True, source='client.sales_contact.id')
    sales_contact_first_name = serializers.CharField(read_only=True, source='client.sales_contact.first_name')
    sales_contact_last_name = serializers.CharField(read_only=True, source='client.sales_contact.last_name')
    sales_contact_email = serializers.CharField(read_only=True, source='client.sales_contact.email')

    class Meta:
        model = Contract
        fields = ['id', 'client', 'client_first_name', 'client_last_name', 'client_email', 'date_created', 'date_updated', 'status', 'amount', 'payment_due', 'sales_contact', 'sales_contact_first_name', 'sales_contact_last_name', 'sales_contact_email']
