from .models import Event


def get_event_from_admin_request(request):
    """
    Factorisation retrieving an event from a request, used several times in admin.py.
    :param request: The HTML request.
    :return: A sales contact (CustomUser object).
    """
    event_pk = int(request.resolver_match.kwargs['object_id'])
    event = Event.objects.get(pk=event_pk)
    return event


def get_sales_contact_of_client_from_event(event):
    """
    Factorisation retrieving sales contact of the client of an event, used several times in admin.py.
    :param event: An Event object.
    :return: A sales contact (CustomUser object).
    """
    client = event.client
    sales_contact = client.sales_contact
    return sales_contact
