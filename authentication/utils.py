from .models import Client


def get_sales_contact_from_admin_request(request):
    """
    Factorisation retrieving sales contact of a client, used several times in admin.py.
    :param request: The HTML request.
    :return: A sales contact (CustomUser object).
    """
    client_pk = int(request.resolver_match.kwargs['object_id'])
    client = Client.objects.get(pk=client_pk)
    sales_contact = client.sales_contact
    return sales_contact


def get_sales_contact_from_event_or_contract(self, object, logger):
    """
    Factorisation retrieving sales contact of the client of a contract or event.
    Used several times in permissions.py.
    :return: A sales contact (CustomUser object).
    """
    try:
        client = object.client
    except AttributeError as e:
        self.message = e
        logger.warning(f"The event has no client!: {e}")
        return False
    try:
        sales_contact = client.sales_contact
    except AttributeError as e:
        self.message = e
        logger.warning(f"The client has no sales_contact!: {e}")
        return False
    return sales_contact
