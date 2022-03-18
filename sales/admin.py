import logging

from django.contrib import admin
from .models import Contract
from .utils import get_sales_contact_of_client_of_contract_from_admin_request

logger = logging.getLogger(__name__)


class ContractAdmin(admin.ModelAdmin):
    """
    Handling admin interface for contracts.
    """
    list_display = ('client', 'sales_contact', 'date_created', 'date_updated', 'status', 'amount', 'payment_due')
    search_fields = ('client__first_name', 'client__last_name', 'client__email', 'client__company_name',
                     'client__sales_contact', 'date_created__startswith', 'amount')

    def get_actions(self, request):
        """
        Overrides get_actions of ModelAdmin to implement removal of delete actions in admin list view for non superusers.
        :param request: The HTML request.
        :return: a list of actions
        """
        actions = super().get_actions(request)
        if not request.user.is_superuser and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        """
        Overrides get_readonly_fields of ModelAdmin to implement deactivation of modification of fields in
        admin detailed view for non-authorized users, as only superusers and sales_contact of the client of the contract
        are authorized to modify it.
        :param request: The HTML request.
        :return: A list of read only fields.
        """
        read_only_fields = super().get_readonly_fields(request)
        try:
            sales_contact = get_sales_contact_of_client_of_contract_from_admin_request(request)
            if request.user != sales_contact and not request.user.is_superuser:
                read_only_fields = read_only_fields + ('client', 'date_created', 'date_updated', 'status', 'amount',
                                                       'payment_due')
        except KeyError:
            logger.warning("User tried to access a contract page that does not exist.")
        return read_only_fields

    def has_delete_permission(self, request, obj=None):
        """
        Overrides get_readonly_fields of ModelAdmin to implement deactivation of delete button in admin detailed view
        for non-authorized users, as only superusers and sales_contact of the client of a contract are authorized to
        modify it.
        :param request: The HTML request.
        :return: A boolean determining if the user has permission to delete.
        """
        if request.resolver_match.url_name == 'sales_contract_change':
            try:
                sales_contact = get_sales_contact_of_client_of_contract_from_admin_request(request)
                return request.user == sales_contact or request.user.is_superuser
            except KeyError:
                logger.warning("User tried to access a contract page that does not exist.")
        return super().has_delete_permission(request)


admin.site.register(Contract, ContractAdmin)
