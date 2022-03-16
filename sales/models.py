from django.db import models
from django.conf import settings

from authentication.models import Client


class Contract(models.Model):
    """
    Contract model.
    Two foreign keys:
    - A sale user
    - A client.
    """
    client = models.ForeignKey(blank=True, null=True, to='authentication.CLIENT', on_delete=models.PROTECT, related_name='contracts')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(blank=True)
    payment_due = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.client)

    @property
    def sales_contact(self):
        return Client.objects.get(contracts=self).sales_contact
