from django.db import models
from django.conf import settings


class Contract(models.Model):
    """
    Contract model.
    Two foreign keys:
    - A sale user
    - A client.
    """
    sales_contact = models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    client = models.ForeignKey(null=True, to='authentification.CLIENT', on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(null=True)
    payment_due = models.DateTimeField(null=True)
