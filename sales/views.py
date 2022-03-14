from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Contract
from .serializers import ContractSerializer
from .filters import ContractFilter
from authentication.permissions import IsInSalesTeam, IsContractSClientResponsible


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter


    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam()]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam(), IsContractSClientResponsible()]
        return permission_classes
