from django.contrib import admin
from .models import Event
from .utils import get_event_from_admin_request, get_sales_contact_of_client_from_event


class EventAdmin(admin.ModelAdmin):
    list_display = ('client', 'support_contact', 'date_created', 'date_updated', 'status', 'attendees', 'event_date', 'notes')
    search_fields = ('client__first_name', 'client__last_name', 'client__email', 'client__company_name', 'event_date__startswith')

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
            event = get_event_from_admin_request(request)
            sales_contact = get_sales_contact_of_client_from_event(event)
            if request.user != event.support_contact and request.user != sales_contact and not request.user.is_superuser:
                read_only_fields = read_only_fields + (
                    'client', 'support_contact', 'date_created', 'date_updated',
                    'status', 'attendees', 'event_date', 'notes')
        except KeyError:
            pass
        return read_only_fields

    def has_delete_permission(self, request, obj=None):
        if request.resolver_match.url_name == 'support_event_change':
            try:
                event = get_event_from_admin_request(request)
                sales_contact = get_sales_contact_of_client_from_event(event)
                return request.user == event.support_contact or request.user == sales_contact or request.user.is_superuser
            except KeyError:
                pass
        return super().has_delete_permission(request)


admin.site.register(Event, EventAdmin)
