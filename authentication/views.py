from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Client
from .serializers import ClientSerializer
from .permissions import IsClientResponsible, IsInSalesTeam
from .filters import ClientFilter


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam()]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam(), IsClientResponsible()]
        return permission_classes
