from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from halls.api.views import HallTypeViewSet, PropertyViewSet, HallViewSet
from orders.api.views import OrderView, OrderStatusView, OrderHistoryView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('hall-type', HallTypeViewSet)
router.register('property', PropertyViewSet)
router.register('hall', HallViewSet)
router.register('order', OrderView)
router.register('order-status', OrderStatusView)
router.register('order-history', OrderHistoryView)
urlpatterns = router.urls
