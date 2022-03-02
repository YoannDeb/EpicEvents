from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, ClientViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('', include(router.urls))
]
