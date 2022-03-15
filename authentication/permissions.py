from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from sales.models import Contract
from support.models import Event


class IsInSalesTeam(BasePermission):
    message = "Access forbidden: You are not part of sales team."

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sales').exists()


class IsInSupportTeam(BasePermission):
    message = "Access forbidden: You are not part of support team."

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Support').exists()


class IsInSalesOrSupportTeam(BasePermission):
    message = "Access forbidden: You are not part of sales or support team"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sales').exists() or request.user.groups.filter(name='Support').exists()


class IsClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of this client."

    def has_permission(self, request, view):
        client_pk = int(request.resolver_match.kwargs['pk'])
        client = Client.objects.get(pk=client_pk)

        return request.user == client.sales_contact


class IsContractSClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of the contract's client."

    def has_permission(self, request, view):
        contract_pk = int(request.resolver_match.kwargs['pk'])
        contract = Contract.objects.get(pk=contract_pk)
        client = contract.client
        sales_contact = client.sales_contact

        return request.user == sales_contact


class IsEventResponsibleOrIsEventSClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of this event or it's client."

    def has_permission(self, request, view):
        event_pk = int(request.resolver_match.kwargs['pk'])
        event = Event.objects.get(pk=event_pk)
        client = event.client
        sales_contact = client.sales_contact

        return request.user == event.support_contact or request.user == sales_contact
