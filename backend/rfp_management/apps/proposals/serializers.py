"""Proposals app - serializers"""
from rest_framework import serializers
from .models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            'id', 'rfp_id', 'vendor_id', 'vendor_name', 'proposal_content',
            'parsed_data', 'price', 'delivery_time', 'warranty', 'payment_terms',
            'score', 'evaluation', 'received_at', 'updated_at', 'email_message_id',
            'status'
        ]
        read_only_fields = ['received_at', 'updated_at']
