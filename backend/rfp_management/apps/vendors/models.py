"""Vendors app - models for vendor management"""
from django.db import models


class Vendor(models.Model):
    """Model for managing vendor information"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vendors'

    def __str__(self):
        return self.name
