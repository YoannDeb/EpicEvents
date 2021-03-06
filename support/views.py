from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event
from .serializers import EventSerializer
from authentication.permissions import IsInSalesTeam, IsInSalesOrSupportTeam, IsEventResponsibleOrIsEventSClientResponsible
from .filters import EventFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_permissions(self):
        """
        Overload of get_permission method of parent class ModelViewSet.
        Defines permission_classes depending on the action.
        - List or retrieve for authenticated users.
        - Create for sales team members.
        - Modifications for support team member which is responsible for the client or sales team member which is
        responsible of the client of the event.
        :return: A list of permissions.
        """
        permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam()]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesOrSupportTeam(),
                                  IsEventResponsibleOrIsEventSClientResponsible()]
        return permission_classes
