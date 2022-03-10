from django.contrib import admin
from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_created', 'date_updated', 'status', 'amount', 'payment_due')

    search_fields = ('client__first_name', 'client__last_name', 'client__email', 'client__company_name', 'date_created__startswith', 'amount')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            try:
                del actions['delete_selected']
            except KeyError:
                pass
        return actions

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = super().get_readonly_fields(request)
        try:
            contract_pk = int(request.resolver_match.kwargs['object_id'])
            contract = Contract.objects.get(pk=contract_pk)
            client = contract.client
            sales_contact = client.sales_contact
            if request.user != sales_contact:
                read_only_fields = read_only_fields + ('client', 'date_created', 'date_updated', 'status', 'amount', 'payment_due')
        except KeyError:
            pass
        return read_only_fields

    def has_delete_permission(self, request, obj=None):
        if request.resolver_match.url_name == 'sales_contract_change':
            try:
                contract_pk = int(request.resolver_match.kwargs['object_id'])
                contract = Contract.objects.get(pk=contract_pk)
                client = contract.client
                sales_contact = client.sales_contact
                return request.user == sales_contact or request.user.is_superuser
            except KeyError:
                pass
        return super().has_delete_permission(request)


admin.site.register(Contract, ContractAdmin)
