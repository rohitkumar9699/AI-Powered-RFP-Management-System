"""AI app - views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import AIService


class AIViewSet(viewsets.ViewSet):
    """ViewSet for AI operations"""

    @action(detail=False, methods=['post'])
    def parse_natural_language(self, request):
        """Parse natural language input into RFP structure"""
        description = request.data.get('description', '')
        
        if not description:
            return Response(
                {'error': 'description is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ai_service = AIService()
            result = ai_service.parse_natural_language_to_rfp(description)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def parse_proposal(self, request):
        """Parse proposal email content"""
        proposal_content = request.data.get('proposal_content', '')
        
        if not proposal_content:
            return Response(
                {'error': 'proposal_content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ai_service = AIService()
            result = ai_service.parse_proposal(proposal_content)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def evaluate_proposals(self, request):
        """Evaluate multiple proposals"""
        rfp_requirements = request.data.get('rfp_requirements', {})
        proposals = request.data.get('proposals', [])
        
        if not proposals:
            return Response(
                {'error': 'proposals list is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ai_service = AIService()
            result = ai_service.evaluate_proposals(rfp_requirements, proposals)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
