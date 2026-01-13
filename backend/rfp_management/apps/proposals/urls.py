"""Proposals app - urls"""
from django.urls import path, include
from rest_framework import routers
from .views import ProposalViewSet

router = routers.DefaultRouter()
router.register(r'', ProposalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
