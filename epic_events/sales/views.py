from rest_framework import viewsets, permissions

from .models import Contract
from .serializers import ContractSerializer
from authentification.permissions import IsInSalesTeam, IsContractSClientResponsible


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam()]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsContractSClientResponsible()]
        return permission_classes
