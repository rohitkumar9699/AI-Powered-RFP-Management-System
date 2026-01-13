"""Proposals app - views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Proposal
from .serializers import ProposalSerializer
from rfp_management.apps.rfps.models import RFP
from rfp_management.apps.ai.services import AIService


class ProposalViewSet(viewsets.ModelViewSet):
    """ViewSet for Proposal management"""
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    @action(detail=False, methods=['get'])
    def by_rfp(self, request):
        """Get all proposals for a specific RFP"""
        rfp_id = request.query_params.get('rfp_id')
        
        if not rfp_id:
            return Response(
                {'error': 'rfp_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        proposals = Proposal.objects.filter(rfp_id=rfp_id).order_by('-received_at')
        serializer = self.get_serializer(proposals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def parse(self, request, pk=None):
        """Parse proposal content using AI"""
        proposal = self.get_object()
        
        try:
            ai_service = AIService()
            parsed_data = ai_service.parse_proposal(proposal.proposal_content)
            
            proposal.parsed_data = parsed_data
            proposal.price = parsed_data.get('price')
            proposal.delivery_time = parsed_data.get('delivery_time', '')
            proposal.warranty = parsed_data.get('warranty', '')
            proposal.payment_terms = parsed_data.get('payment_terms', '')
            proposal.status = 'PARSED'
            proposal.save()

            serializer = self.get_serializer(proposal)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def compare_and_evaluate(self, request):
        """Compare and evaluate proposals for an RFP"""
        rfp_id = request.data.get('rfp_id')
        
        if not rfp_id:
            return Response(
                {'error': 'rfp_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rfp = RFP.objects.get(id=rfp_id)
            proposals = Proposal.objects.filter(rfp_id=rfp_id)

            if not proposals.exists():
                return Response(
                    {'error': 'No proposals found for this RFP'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Prepare data for AI evaluation
            proposal_data = []
            for prop in proposals:
                proposal_data.append({
                    'vendor_name': prop.vendor_name,
                    'price': float(prop.price) if prop.price else None,
                    'delivery_time': prop.delivery_time,
                    'warranty': prop.warranty,
                    'payment_terms': prop.payment_terms,
                    'parsed_data': prop.parsed_data
                })

            ai_service = AIService()
            evaluation = ai_service.evaluate_proposals(
                rfp_requirements=rfp.requirements,
                proposals=proposal_data
            )

            # Update proposals with evaluation scores
            for prop in proposals:
                vendor_eval = evaluation['evaluations'].get(prop.vendor_name, {})
                prop.score = vendor_eval.get('score', 0)
                prop.evaluation = vendor_eval
                prop.status = 'EVALUATED'
                prop.save()

            # Fetch updated proposals
            updated_proposals = Proposal.objects.filter(rfp_id=rfp_id)
            serializer = self.get_serializer(updated_proposals, many=True)
            
            return Response({
                'summary': evaluation.get('summary', ''),
                'recommendation': evaluation.get('recommendation', ''),
                'proposals': serializer.data
            })
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
