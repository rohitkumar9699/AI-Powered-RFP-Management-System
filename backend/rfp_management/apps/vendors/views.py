"""Vendors app - views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
    """ViewSet for Vendor management"""
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active vendors"""
        vendors = Vendor.objects.filter(active=True)
        serializer = self.get_serializer(vendors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle vendor active status"""
        vendor = self.get_object()
        vendor.active = not vendor.active
        vendor.save()
        return Response({'status': 'vendor status toggled', 'active': vendor.active})
