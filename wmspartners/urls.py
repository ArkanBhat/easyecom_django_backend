from rest_framework.routers import DefaultRouter
from .views import WmsCustomerViewSet,WmsPartnerViewSet, WmsPartnerApisViewSet, WmsShipmentsViewSet, WmsCustomerAuthViewSet, WmsShipmentLogsViewSet, ShipmentStatusViewSet

router = DefaultRouter()
router.register(r'customers', WmsCustomerViewSet)
router.register(r'partners', WmsPartnerViewSet)
router.register(r'partner-apis', WmsPartnerApisViewSet)
router.register(r'shipments', WmsShipmentsViewSet)
router.register(r'customer-auth', WmsCustomerAuthViewSet)
router.register(r'shipmentlogs', WmsShipmentLogsViewSet)
router.register(r'shipment-status', ShipmentStatusViewSet)



urlpatterns = router.urls
