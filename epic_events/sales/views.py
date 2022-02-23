from rest_framework import viewsets, permissions

from .models import Contract
from .serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        return permission_classes

    def get_queryset(self):
        return Contract.objects.all()
