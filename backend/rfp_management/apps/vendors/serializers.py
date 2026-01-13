"""Vendors app - serializers"""
from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'email', 'contact_person', 'phone',
            'address', 'city', 'country', 'website', 'notes',
            'created_at', 'updated_at', 'active'
        ]
        read_only_fields = ['created_at', 'updated_at']
