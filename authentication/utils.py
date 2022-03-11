from .models import Client


def get_sales_contact_from_admin_request(request):
    client_pk = int(request.resolver_match.kwargs['object_id'])
    client = Client.objects.get(pk=client_pk)
    sales_contact = client.sales_contact
    return sales_contact
