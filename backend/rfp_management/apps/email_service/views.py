"""Email service app - views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import EmailService
from rfp_management.apps.proposals.models import Proposal
from rfp_management.apps.vendors.models import Vendor
from rfp_management.apps.rfps.models import RFP
import re


class EmailServiceViewSet(viewsets.ViewSet):
    """ViewSet for email operations"""

    @action(detail=False, methods=['post'])
    def check_proposals(self, request):
        """Check for incoming proposal emails"""
        try:
            email_service = EmailService()
            emails = email_service.receive_proposal_emails()
            
            received_proposals = []
            
            for email_data in emails:
                sender = email_service.extract_vendor_email(email_data['sender'])
                
                # Try to match vendor
                try:
                    vendor = Vendor.objects.get(email=sender)
                except Vendor.DoesNotExist:
                    vendor = None
                
                # Try to find RFP from subject or email content
                rfp_id = self._extract_rfp_id(email_data['subject'], email_data['body'])
                
                if vendor and rfp_id:
                    # Create proposal
                    proposal = Proposal.objects.create(
                        rfp_id=rfp_id,
                        vendor_id=str(vendor.id),
                        vendor_name=vendor.name,
                        proposal_content=email_data['body'],
                        email_message_id=email_data['message_id'],
                        status='RECEIVED'
                    )
                    
                    received_proposals.append({
                        'id': str(proposal.id),
                        'vendor': vendor.name,
                        'rfp_id': rfp_id,
                        'subject': email_data['subject']
                    })
            
            return Response({
                'message': f'Checked {len(emails)} emails',
                'proposals_received': received_proposals
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def send_rfp(self, request):
        """Send RFP to vendor"""
        rfp_id = request.data.get('rfp_id')
        vendor_id = request.data.get('vendor_id')
        
        if not rfp_id or not vendor_id:
            return Response(
                {'error': 'rfp_id and vendor_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            rfp = RFP.objects.get(id=rfp_id)
            email_service = EmailService()
            email_service.send_rfp_to_vendor(rfp, vendor_id)
            
            return Response({
                'message': f'RFP sent successfully to vendor {vendor_id}'
            }, status=status.HTTP_200_OK)
            
        except RFP.DoesNotExist:
            return Response(
                {'error': 'RFP not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _extract_rfp_id(self, subject: str, body: str) -> str:
        """
        Extract RFP ID from email subject or body.
        
        Args:
            subject: Email subject
            body: Email body
            
        Returns:
            str: RFP ID if found, else empty string
        """
        # Try to find RFP ID pattern
        pattern = r'RFP[:\s]+(\d+)'
        
        # Search in subject
        match = re.search(pattern, subject, re.IGNORECASE)
        if match:
            return match.group(1)
        
        # Search in body
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return ''
