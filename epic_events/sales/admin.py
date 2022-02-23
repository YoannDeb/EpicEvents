from django.contrib import admin
from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    list_display = ('client', 'sales_contact', 'date_created', 'date_updated', 'status', 'amount', 'payment_due')


admin.site.register(Contract, ContractAdmin)
