from django.db import models
from django.conf import settings


class Event(models.Model):
    """
    Event model.
    Two foreign keys:
    - A sale user
    - A client.
    """

    FUTURE = 'FT'
    ONGOING = 'OG'
    FINISHED = 'FI'

    STATUS_CHOICES = [
        (FUTURE, 'Future'),
        (ONGOING, 'Ongoing'),
        (FINISHED, 'Finished')
    ]

    client = models.ForeignKey(blank=True, null=True, to='authentication.CLIENT', on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        default=FUTURE, max_length=2, choices=STATUS_CHOICES,
        error_messages={
            'invalid_choice': f'Type must be between those choices: '
                              f'{FUTURE} for future events, {ONGOING} for ongoing events and '
                              f'{FINISHED} for finished events'
        }
    )
    attendees = models.IntegerField(blank=True)
    event_date = models.DateTimeField(blank=True)
    notes = models.TextField(max_length=5000, blank=True)
    support_contact = models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.client)
