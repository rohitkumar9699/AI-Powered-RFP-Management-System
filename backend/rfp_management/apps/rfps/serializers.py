"""RFPs app - serializers"""
from rest_framework import serializers
from .models import RFP, RFPField


class RFPFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFPField
        fields = ['id', 'rfp_id', 'field_name', 'field_value', 'field_type']


class RFPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFP
        fields = [
            'id', 'title', 'description', 'requirements', 'budget', 'deadline',
            'created_at', 'updated_at', 'status', 'selected_vendors', 'awarded_vendor',
            'natural_language_input'
        ]
        read_only_fields = ['created_at', 'updated_at']
