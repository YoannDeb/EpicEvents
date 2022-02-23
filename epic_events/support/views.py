from rest_framework import viewsets, permissions

from .models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        return permission_classes

    def get_queryset(self):
        return Event.objects.all()

