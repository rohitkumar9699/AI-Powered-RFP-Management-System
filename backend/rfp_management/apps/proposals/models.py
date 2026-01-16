"""Proposals app - models for vendor proposals"""
from django.db import models


class Proposal(models.Model):
    """Model for vendor proposals in response to RFPs"""
    rfp_id = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    proposal_content = models.TextField()
    parsed_data = models.JSONField(default=dict)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    delivery_time = models.CharField(max_length=255, blank=True)
    warranty = models.CharField(max_length=255, blank=True)
    payment_terms = models.CharField(max_length=255, blank=True)
    score = models.FloatField(null=True, blank=True)
    evaluation = models.JSONField(default=dict)
    received_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_message_id = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('RECEIVED', 'Received'),
            ('PARSED', 'Parsed'),
            ('EVALUATED', 'Evaluated'),
            ('ACCEPTED', 'Accepted'),
        ],
        default='RECEIVED'
    )

    class Meta:
        db_table = 'proposals'

    def __str__(self):
        return f'Proposal from {self.vendor_name} for RFP {self.rfp_id}'
