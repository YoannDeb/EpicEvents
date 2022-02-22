from django.db import models
from django.conf import settings


class Event(models.Model):
    """
    Event model.
    Two foreign keys:
    - A sale user
    - A client.
    """
    support_contact = models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    client = models.ForeignKey(null=True, to='authentification.CLIENT', on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)
    attendees = models.IntegerField(null=True)
    event_date = models.DateTimeField(null=True)
    notes = models.TextField(max_length=5000, null=True)
