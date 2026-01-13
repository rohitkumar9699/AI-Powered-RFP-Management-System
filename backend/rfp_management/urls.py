"""
URL Configuration for rfp_management project.
"""
from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('api/vendors/', include('rfp_management.apps.vendors.urls')),
    path('api/rfps/', include('rfp_management.apps.rfps.urls')),
    path('api/proposals/', include('rfp_management.apps.proposals.urls')),
    path('api/ai/', include('rfp_management.apps.ai.urls')),
    path('api/email/', include('rfp_management.apps.email_service.urls')),
]
