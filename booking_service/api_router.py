from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from halls.api.views import HallTypeViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('hall-type', HallTypeViewSet)

urlpatterns = router.urls
