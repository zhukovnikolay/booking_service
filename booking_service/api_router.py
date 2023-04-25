from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from halls.api.views import HallTypeViewSet, PropertyViewSet, HallViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('hall-type', HallTypeViewSet)
router.register('property', PropertyViewSet)
router.register('hall', HallViewSet)

urlpatterns = router.urls
