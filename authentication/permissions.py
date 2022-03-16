import logging

from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from sales.models import Contract
from support.models import Event

from .utils import get_sales_contact_from_event_or_contract

logger = logging.getLogger(__name__)


class IsInSalesTeam(BasePermission):
    message = "Access forbidden: You are not part of sales team."

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sales').exists() or request.user.is_superuser


class IsInSupportTeam(BasePermission):
    message = "Access forbidden: You are not part of support team."

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Support').exists() or request.user.is_superuser


class IsInSalesOrSupportTeam(BasePermission):
    message = "Access forbidden: You are not part of sales or support team"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Sales').exists() or request.user.groups.filter(name='Support').exists() or request.user.is_superuser


class IsClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of this client."

    def has_permission(self, request, view):
        client_pk = int(request.resolver_match.kwargs['pk'])
        try:
            client = Client.objects.get(pk=client_pk)
        except ObjectDoesNotExist as e:
            self.message = e
            logger.info(f"User tried to access a client that does not exist: {e}")
            return False
        return request.user == client.sales_contact or request.user.is_superuser


class IsContractSClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of the contract's client."

    def has_permission(self, request, view):
        contract_pk = int(request.resolver_match.kwargs['pk'])
        try:
            contract = Contract.objects.get(pk=contract_pk)
        except ObjectDoesNotExist as e:
            self.message = e
            logger.info(f"User tried to access a contract that does not exist: {e}")
            return False
        sales_contact = get_sales_contact_from_event_or_contract(self, contract, logger)

        return request.user == sales_contact or request.user.is_superuser


class IsEventResponsibleOrIsEventSClientResponsible(BasePermission):
    message = "Access forbidden: You are not responsible of this event or it's client."

    def has_permission(self, request, view):
        event_pk = int(request.resolver_match.kwargs['pk'])
        try:
            event = Event.objects.get(pk=event_pk)
        except ObjectDoesNotExist as e:
            self.message = e
            logger.warning(f"User tried to access an event that does not exist: {e}")
            return False
        sales_contact = get_sales_contact_from_event_or_contract(self, event, logger)

        return request.user == event.support_contact or request.user == sales_contact or request.user.is_superuser
