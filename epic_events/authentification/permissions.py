from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser, Client
from sales.models import Contract
from support.models import Event


class IsInSalesTeam(BasePermission):
    message = "Access forbidden: You are not part of sales team."

    def has_permission(self, request, view):
        # return 'Sales' in list(request.user.groups.all().values_list('name', flat=True))
        return request.user.groups.filter(name='Sales').exists()


class IsClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of this client."

    def has_permission(self, request, view):
        client_pk = int(request.resolver_match.kwargs['client_pk'])
        client = Client.objects.get(pk=client_pk)

        return request.user == client.sales_contact


class IsContractSClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of the contract's client."

    def has_permission(self, request, view):
        contract_pk = int(request.resolver_match.kwargs['contract_pk'])
        contract = Contract.objects.get(pk=contract_pk)
        client = contract.client
        sales_contact = client.sales_contact

        return request.user == sales_contact


class IsEventSClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of the event's client."

    def has_permission(self, request, view):
        event_pk = int(request.resolver_match.kwargs['event_pk'])
        event = Event.objects.get(pk=event_pk)
        client = event.client
        sales_contact = client.sales_contact

        return request.user == sales_contact


class IsInSupportTeam(BasePermission):
    message = "Access forbidden: You are not part of sales team."

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Support').exists()


class IsEventResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of this event."

    def has_permission(self, request, view):
        event_pk = int(request.resolver_match.kwargs['event_pk'])
        event = Event.objects.get(pk=event_pk)

        return request.user == event.support_contact
