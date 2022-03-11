from .models import Contract


def get_sales_contact_of_client_of_contract_from_admin_request(request):
    contract_pk = int(request.resolver_match.kwargs['object_id'])
    contract = Contract.objects.get(pk=contract_pk)
    client = contract.client
    sales_contact = client.sales_contact
    return sales_contact
