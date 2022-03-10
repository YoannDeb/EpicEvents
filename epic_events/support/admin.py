from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('client', 'support_contact', 'date_created', 'date_updated', 'status', 'attendees', 'event_date', 'notes')

    search_fields = ('client__first_name', 'client__last_name', 'client__email', 'client__company_name', 'event_date__startswith')

    # def get_actions(self, request):
    #     client_pk = int(request.resolver_match.kwargs['pk'])
    #     client = Client.objects.get(pk=client_pk)
    #     actions = super().get_actions(request)
    #     if request.user != client.sales_contact:
    #         del actions['delete_selected']
    #     print(actions)
    #     del actions['delete_selected']
    #     return actions

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
            event_pk = int(request.resolver_match.kwargs['object_id'])
            event = Event.objects.get(pk=event_pk)
            client = event.client
            sales_contact = client.sales_contact
            if request.user != event.support_contact and request.user != sales_contact:
                read_only_fields = read_only_fields + (
                    'client', 'support_contact', 'date_created', 'date_updated',
                    'status', 'attendees', 'event_date', 'notes')
        except KeyError:
            pass
        return read_only_fields

    def has_delete_permission(self, request, obj=None):
        if request.resolver_match.url_name == 'support_event_change':
            try:
                event_pk = int(request.resolver_match.kwargs['object_id'])
                event = Event.objects.get(pk=event_pk)
                client = event.client
                sales_contact = client.sales_contact
                return request.user == event.support_contact or request.user == sales_contact or request.user.is_superuser
            except KeyError:
                pass
        return super().has_delete_permission(request)


admin.site.register(Event, EventAdmin)
