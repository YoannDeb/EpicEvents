from rest_framework import serializers

from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'sales_contact', 'client', 'date_created', 'date_updated', 'status', 'amount', 'payment_due']


class CreateContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['sales_contact', 'client', 'status', 'amount', 'payment_due']