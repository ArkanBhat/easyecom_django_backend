from rest_framework import serializers
from .models import WmsCustomer, WmsPartner, WmsPartnerApis, WmsShipments, WmsCustomerAuth, WmsShipmentLogs, ShipmentStatus


class WmsCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WmsCustomer
        fields = '__all__'


class WmsPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WmsPartner
        fields = '__all__'

class WmsPartnerApisSerializer(serializers.ModelSerializer):
    class Meta:
        model = WmsPartnerApis
        fields = '__all__'

class WmsShipmentsSerializer(serializers.ModelSerializer):

    # This is for reading (nested output)
    customer = WmsCustomerSerializer(read_only=True)

    # This is for writing (accept ID)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=WmsCustomer.objects.all(),
        source='customer',
        write_only=True
    )

    class Meta:
        model = WmsShipments
        fields = '__all__'
       

class WmsCustomerAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = WmsCustomerAuth
        fields = '__all__'

class WmsShipmentLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WmsShipmentLogs
        fields = '__all__'

class ShipmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentStatus
        fields = "__all__"


