"""RFPs app - urls"""
from django.urls import path, include
from rest_framework import routers
from .views import RFPViewSet

router = routers.DefaultRouter()
router.register(r'', RFPViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
