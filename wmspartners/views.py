from rest_framework import viewsets
from .models import WmsCustomer
from .serializers import WmsCustomerSerializer


class WmsCustomerViewSet(viewsets.ModelViewSet):
    queryset = WmsCustomer.objects.all()
    serializer_class = WmsCustomerSerializer

from rest_framework import viewsets
from .models import WmsPartner
from .serializers import WmsPartnerSerializer


class WmsPartnerViewSet(viewsets.ModelViewSet):
    queryset = WmsPartner.objects.all()
    serializer_class = WmsPartnerSerializer

from rest_framework import viewsets
from .models import WmsPartnerApis
from .serializers import WmsPartnerApisSerializer


class WmsPartnerApisViewSet(viewsets.ModelViewSet):
    queryset = WmsPartnerApis.objects.all()
    serializer_class = WmsPartnerApisSerializer

from rest_framework import viewsets
from .models import WmsShipments
from .serializers import WmsShipmentsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class WmsShipmentsViewSet(viewsets.ModelViewSet):
    queryset = WmsShipments.objects.all()
    serializer_class = WmsShipmentsSerializer
    
    @action(detail=True, methods=['post'])
    def send_to_carrier(self, request, pk=None):
        shipment = self.get_object()

    # Simulated request payload
        shipment.request = f"Sending AWB {shipment.awb} to carrier"

    # Simulated carrier response
        shipment.response = "Shipment accepted by carrier"
    
    # Update status to In Transit (code = 2)
        shipment.status_id = 2
        shipment.save()

        return Response({
        "message": "Shipment sent successfully",
        "status": shipment.status.name
    })
    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        shipment = self.get_object()

    # Only allow delivery if currently In Transit
        if shipment.status.code != 2:
            return Response({"error": "Only In Transit shipments can be delivered"},status=400)
        shipment.status_id = 3  # Delivered
        shipment.save()

        return Response({
        "message": "Shipment delivered successfully",
        "status": shipment.status.name
    })
    @action(detail=True, methods=['post'])
    def mark_failed(self, request, pk=None):
        shipment = self.get_object()

    # Only allow failure if In Transit
        if shipment.status.code != 2:
            return Response(
            {"error": "Only In Transit shipments can fail"},
            status=400
        )

        shipment.status_id = 4  # Failed
        shipment.save()

        return Response({
        "message": "Shipment marked as failed",
        "status": shipment.status.name
    })
    @action(detail=True, methods=['get'])
    def track(self, request, pk=None):
        shipment = self.get_object()

        return Response({
        "awb": shipment.awb,
        "order": shipment.order,
        "status": shipment.status.name,
        "request": shipment.request,
        "response": shipment.response
    })

    @action(detail=True, methods=['get'])
    def print_label(self, request, pk=None):
        shipment = self.get_object()

        return Response({
        "awb": shipment.awb,
        "label_url": f"http://localhost:8000/labels/{shipment.awb}.pdf",
        "message": "Label generated successfully"
    })





from rest_framework import viewsets
from .models import WmsCustomerAuth
from .serializers import WmsCustomerAuthSerializer

class WmsCustomerAuthViewSet(viewsets.ModelViewSet):
    queryset = WmsCustomerAuth.objects.all()
    serializer_class = WmsCustomerAuthSerializer

from rest_framework import viewsets
from .models import WmsShipmentLogs
from .serializers import WmsShipmentLogsSerializer

class WmsShipmentLogsViewSet(viewsets.ModelViewSet):
    queryset = WmsShipmentLogs.objects.all()
    serializer_class = WmsShipmentLogsSerializer

from .models import ShipmentStatus
from .serializers import ShipmentStatusSerializer

class ShipmentStatusViewSet(viewsets.ModelViewSet):
    queryset = ShipmentStatus.objects.all()
    serializer_class = ShipmentStatusSerializer
