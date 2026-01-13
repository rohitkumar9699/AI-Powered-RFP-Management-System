"""RFPs app - models for RFP management"""
from django.db import models
from djongo import models as mongo_models
import json


class RFP(models.Model):
    """Model for Request for Proposal"""
    id = mongo_models.ObjectIdField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = mongo_models.JSONField(default=dict)  # Structured requirements
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('DRAFT', 'Draft'),
            ('SENT', 'Sent to Vendors'),
            ('CLOSED', 'Closed'),
            ('AWARDED', 'Awarded')
        ],
        default='DRAFT'
    )
    selected_vendors = mongo_models.JSONField(default=list)  # List of vendor IDs
    awarded_vendor = models.CharField(max_length=255, blank=True, null=True)
    natural_language_input = models.TextField(blank=True)  # Original user input

    class Meta:
        db_table = 'rfps'

    def __str__(self):
        return self.title


class RFPField(models.Model):
    """Model for tracking structured fields in an RFP"""
    id = mongo_models.ObjectIdField()
    rfp_id = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    field_value = models.TextField()
    field_type = models.CharField(max_length=50)  # text, number, date, array, etc.

    class Meta:
        db_table = 'rfp_fields'
