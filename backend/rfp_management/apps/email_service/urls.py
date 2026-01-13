"""Email service app - urls"""
from django.urls import path
from .views import EmailServiceViewSet

urlpatterns = [
    path('check-proposals/', EmailServiceViewSet.as_view({'post': 'check_proposals'})),
    path('send-rfp/', EmailServiceViewSet.as_view({'post': 'send_rfp'})),
]
