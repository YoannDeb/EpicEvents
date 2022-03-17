import logging

from django.contrib import admin
from .models import Event
from .utils import get_event_from_admin_request, get_sales_contact_of_client_from_event

logger = logging.getLogger(__name__)


class EventAdmin(admin.ModelAdmin):
    """
    Handling admin interface for events.
    """
    list_display = ('client', 'support_contact', 'date_created', 'date_updated', 'status', 'attendees', 'event_date', 'notes')
    search_fields = ('client__first_name', 'client__last_name', 'client__email', 'client__company_name', 'event_date__startswith')

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
        admin detailed view for non-authorized users, as only superusers, support contact of the event and sales contact
        of the client of the contract are authorized to modify it.
        :param request: The HTML request.
        :return: A list of read only fields.
        """
        read_only_fields = super().get_readonly_fields(request)
        try:
            event = get_event_from_admin_request(request)
            sales_contact = get_sales_contact_of_client_from_event(event)
            if request.user != event.support_contact and request.user != sales_contact and not request.user.is_superuser:
                read_only_fields = read_only_fields + (
                    'client', 'support_contact', 'date_created', 'date_updated',
                    'status', 'attendees', 'event_date', 'notes')
        except KeyError:
            logger.warning("User tried to access an event page that does not exist.")
        return read_only_fields

    def has_delete_permission(self, request, obj=None):
        """
        Overrides get_readonly_fields of ModelAdmin to implement deactivation of delete button in admin detailed view
        for non-authorized users, as only superusers, support contact of the event and sales contact of the client of
        the contract are authorized to modify it.
        :param request: The HTML request.
        :return: A boolean determining if the user has permission to delete.
        """
        if request.resolver_match.url_name == 'support_event_change':
            try:
                event = get_event_from_admin_request(request)
                sales_contact = get_sales_contact_of_client_from_event(event)
                return request.user == event.support_contact or request.user == sales_contact or request.user.is_superuser
            except KeyError:
                logger.warning("User tried to access an event page that does not exist.")
        return super().has_delete_permission(request)


admin.site.register(Event, EventAdmin)
