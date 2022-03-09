from django.urls import path, include
from rest_framework import routers

from .views import ContractViewSet

router = routers.DefaultRouter()
router.register(r'contracts', ContractViewSet, basename='ContractViewSet')

urlpatterns = [
    path('', include(router.urls))
]
