from rest_framework import viewsets, permissions

from .models import Client, CustomUser
from .serializers import ClientSerializer, UserSerializer
from .permissions import IsClientResponsible, IsInSalesTeam


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated()]


class ClientViewSet(viewsets.ModelViewSet):
    # queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam()]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsClientResponsible()]
        return permission_classes

    def get_queryset(self):
        queryset = Client.objects.all()
        last_name = self.request.query_params.get('last_name')
        email = self.request.query_params.get('email')
        if last_name and email:
            queryset = queryset.filter(last_name=last_name, email=email)
        elif last_name:
            queryset = queryset.filter(last_name=last_name)
        elif email:
            queryset = queryset.filter(email=email)
        return queryset

