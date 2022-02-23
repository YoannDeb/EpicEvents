from django.db import models
from django.conf import settings


class Event(models.Model):
    """
    Event model.
    Two foreign keys:
    - A sale user
    - A client.
    """
    client = models.ForeignKey(blank=True, null=True, to='authentification.CLIENT', on_delete=models.SET_NULL)
    support_contact = models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    attendees = models.IntegerField(blank=True)
    event_date = models.DateTimeField(blank=True)
    notes = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return str(self.client)
