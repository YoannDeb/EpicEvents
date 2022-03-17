import logging

from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from .models import Client
from sales.models import Contract
from support.models import Event

from .utils import get_sales_contact_from_event_or_contract

logger = logging.getLogger(__name__)


class IsInSalesTeam(BasePermission):
    """
    Permission checking if user is in sales team or is a superuser.
    """
    message = "Access forbidden: You are not part of sales team."

    def has_permission(self, request, view):
        """
        Tests if the user is in sales, or management team.
        :param request: The HTML request.
        :param view: The view where the permission is checked.
        :return: True if the user is either in sales or management team, False if not.
        """
        return request.user.groups.filter(name='Sales').exists() or request.user.is_superuser


class IsInSupportTeam(BasePermission):
    """
    Permission checking if user is in support team or is a superuser.
    """
    message = "Access forbidden: You are not part of support team."

    def has_permission(self, request, view):
        """
        Tests if the user is in support, or management team.
        :param request: The HTML request.
        :param view: The view where the permission is checked.
        :return: True if the user is either in support or management team, False if not.
        """
        return request.user.groups.filter(name='Support').exists() or request.user.is_superuser


class IsInSalesOrSupportTeam(BasePermission):
    """
    Permission checking if user is in sales team or in support team or is a superuser.
    """
    message = "Access forbidden: You are not part of sales or support team"

    def has_permission(self, request, view):
        """
        Tests if the user is in sales, support, or management team.
        :param request: The HTML request.
        :param view: The view where the permission is checked.
        :return: True if the user is either in sales, support or management team, False if not.
        """
        return request.user.groups.filter(name='Sales').exists() or request.user.groups.filter(name='Support').exists() or request.user.is_superuser


class IsClientResponsible(BasePermission):
    """
    Permission checking if the user is the sales contact of a client.
    """
    message = "Access forbidden: You are not responsible of this client."

    def has_permission(self, request, view):
        """
        Tests if the user is the sales contact of a client or a superuser.
        If the client does not exist, a warning message is sent to logging.
        :param request: The HTML request.
        :param view: The view where the permission is checked.
        :return: True if the user is the sales contact of the client, or is superuser. If not or if client does not
        exist, return False.
        """
        client_pk = int(request.resolver_match.kwargs['pk'])
        try:
            client = Client.objects.get(pk=client_pk)
        except ObjectDoesNotExist as e:
            self.message = e
            logger.info(f"User tried to access a client that does not exist: {e}")
            return False
        return request.user == client.sales_contact or request.user.is_superuser


class IsContractSClientResponsible(BasePermission):
    """
    Permission checking if the user is sales contact of the client of a contract.
    """
    message = "Access forbidden: You are not responsible of the contract's client."

    def has_permission(self, request, view):
        """
        Tests if the user is the sales contact of the client of a contract or a superuser.
        If the contract does not exist, a warning message is sent to logging.
        :param request: The HTML request.
        :param view: The view where the permission is checked.
        :return: True if the user is the sales contact of the client of the contract, or is superuser. If not or if
        contract does not exist, return False.
        """
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
    """
    Permission checking if the user is support contact or sales contact of the client of an event.
    """
    message = "Access forbidden: You are not responsible of this event or it's client."

    def has_permission(self, request, view):
        """
        Tests if the user is the support contact or the sales contact of the client of an event, or a superuser.
        If the event does not exist, a warning message is sent to logging.
        :param request: The HTML request.
        :param view: The view where the permission is checked.
        :return: True if the user is the sales contact of the client of the event, or a superuser. If not or if
        cevent does not exist, return False.
        """
        event_pk = int(request.resolver_match.kwargs['pk'])
        try:
            event = Event.objects.get(pk=event_pk)
        except ObjectDoesNotExist as e:
            self.message = e
            logger.warning(f"User tried to access an event that does not exist: {e}")
            return False
        sales_contact = get_sales_contact_from_event_or_contract(self, event, logger)

        return request.user == event.support_contact or request.user == sales_contact or request.user.is_superuser
