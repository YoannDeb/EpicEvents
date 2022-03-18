from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken

from .models import Client, CustomUser
from .serializers import ClientSerializer
from .permissions import IsClientResponsible, IsInSalesTeam
from .filters import ClientFilter


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter

    def get_permissions(self):
        """
        Overload of get_permission method of parent class ModelViewSet.
        Defines permission_classes depending on the action.
        - List or retrieve for authenticated users.
        - Create for sales team members.
        - Modifications for sale team member which is responsible for the client.
        :return: A list of permissions.
        """
        permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [permissions.IsAuthenticated()]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam()]
        if self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated(), IsInSalesTeam(), IsClientResponsible()]
        return permission_classes


# class LogOutAPIView(views.APIView):
#     """
#     Using APIView inheritance as we only need post in this endpoint.
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request):
#         print(request.headers['Authorization'][7:])
#         plain_text_token = request.headers['Authorization'][7:]
#         user_tokens = OutstandingToken.objects.filter(user=request.user)
#
#         print(user_tokens)
#         for token in user_tokens:
#             print(request.headers['Authorization'][7:])
#             print(token.token)
#         user_token.blacklist()
#         return Response(request.data, status=status.HTTP_200_OK)


class LogOutEverywhereAPIView(views.APIView):
    """
    Using APIView inheritance as we only need post in this endpoint.
    TODO: find bug token 4 already listed whereas it is not... must be corrupted data from tests. maybe try to flush token table.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_tokens = OutstandingToken.objects.filter(user=request.user)
        all_tokens = BlacklistedToken.objects.all()
        print(BlacklistedToken)
        black_listed_token_ids = []
        for token in all_tokens:
            print(token)
            black_listed_token_ids.append(token.id)
        print(black_listed_token_ids)
        for token in user_tokens:
            if token.id not in black_listed_token_ids:
                blacklisted = BlacklistedToken(token=token)
                blacklisted.save()
        return Response(request.data, status=status.HTTP_200_OK)
