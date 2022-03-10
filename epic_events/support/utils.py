from .models import Event


def get_event_from_admin_request(request):
    event_pk = int(request.resolver_match.kwargs['object_id'])
    event = Event.objects.get(pk=event_pk)
    return event


def get_sales_contact_of_client_from_event(event):
    client = event.client
    sales_contact = client.sales_contact
    return sales_contact
