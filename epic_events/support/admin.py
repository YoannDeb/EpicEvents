from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('client', 'support_contact', 'date_created', 'date_updated', 'status', 'attendees', 'event_date', 'notes')


admin.site.register(Event, EventAdmin)
