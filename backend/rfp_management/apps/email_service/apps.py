"""Email service app - config"""
from django.apps import AppConfig


class EmailServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rfp_management.apps.email_service'
