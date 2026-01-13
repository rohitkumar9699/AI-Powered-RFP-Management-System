"""RFPs app - views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RFP
from .serializers import RFPSerializer
from rfp_management.apps.ai.services import AIService
from rfp_management.apps.email_service.services import EmailService


class RFPViewSet(viewsets.ModelViewSet):
    """ViewSet for RFP management"""
    queryset = RFP.objects.all()
    serializer_class = RFPSerializer

    @action(detail=False, methods=['post'])
    def create_from_natural_language(self, request):
        """Create RFP from natural language description"""
        natural_language = request.data.get('description', '')
        
        if not natural_language:
            return Response(
                {'error': 'description is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ai_service = AIService()
            structured_rfp = ai_service.parse_natural_language_to_rfp(natural_language)
            
            # Create RFP object
            rfp = RFP.objects.create(
                title=structured_rfp.get('title', 'Untitled RFP'),
                description=natural_language,
                requirements=structured_rfp.get('requirements', {}),
                budget=structured_rfp.get('budget'),
                deadline=structured_rfp.get('deadline'),
                natural_language_input=natural_language,
                status='DRAFT'
            )
            
            serializer = self.get_serializer(rfp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def send_to_vendors(self, request, pk=None):
        """Send RFP to selected vendors"""
        rfp = self.get_object()
        vendor_ids = request.data.get('vendor_ids', [])

        if not vendor_ids:
            return Response(
                {'error': 'vendor_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            email_service = EmailService()
            for vendor_id in vendor_ids:
                email_service.send_rfp_to_vendor(rfp, vendor_id)
            
            rfp.selected_vendors = vendor_ids
            rfp.status = 'SENT'
            rfp.save()

            serializer = self.get_serializer(rfp)
            return Response(
                {'message': 'RFP sent to vendors', 'rfp': serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def award(self, request, pk=None):
        """Award RFP to a vendor"""
        rfp = self.get_object()
        vendor_id = request.data.get('vendor_id')

        if not vendor_id:
            return Response(
                {'error': 'vendor_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rfp.awarded_vendor = vendor_id
        rfp.status = 'AWARDED'
        rfp.save()

        serializer = self.get_serializer(rfp)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close RFP"""
        rfp = self.get_object()
        rfp.status = 'CLOSED'
        rfp.save()

        serializer = self.get_serializer(rfp)
        return Response(serializer.data, status=status.HTTP_200_OK)
