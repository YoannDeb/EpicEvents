from django.db import models
from django.conf import settings


class Contract(models.Model):
    """
    Contract model.
    Two foreign keys:
    - A sale user
    - A client.
    """
    client = models.ForeignKey(blank=True, null=True, to='authentification.CLIENT', on_delete=models.SET_NULL)
    sales_contact = models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(blank=True)
    payment_due = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.client)
