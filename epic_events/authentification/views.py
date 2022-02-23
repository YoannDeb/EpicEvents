from rest_framework import viewsets, permissions

from .models import Client, CustomUser
from .serializers import ClientSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        return permission_classes

    def get_queryset(self):
        return CustomUser.objects.all()


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        return permission_classes

    def get_queryset(self):
        return Client.objects.all()

