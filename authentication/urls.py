from django.urls import path, include
from rest_framework import routers

from .views import ClientViewSet, LogOutEverywhereAPIView

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='ClientViewSet')

urlpatterns = [
    path('', include(router.urls)),
    path('logouteverywhere/', LogOutEverywhereAPIView.as_view())
]
