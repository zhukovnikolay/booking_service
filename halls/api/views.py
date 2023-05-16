import json

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from orders.api.serializers import OrderSerializer
from .serializers import HallTypeSerializer, PropertySerializer, HallSerializer, HallFavoriteSerializer, EventTypeSerializer
from halls.models import HallType, Property, Hall, HallProperty, HallFavorite, EventType


class HallTypeViewSet(ModelViewSet):
    serializer_class = HallTypeSerializer
    queryset = HallType.objects.all()


class PropertyViewSet(ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()


class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.increase_view_count()
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.data._mutable = True
        data = request.data
        properties = data.get('properties', None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if properties:
            properties = json.loads(properties)
            properties = {hall_property['property_name']: hall_property['property_value'] for hall_property in properties}
            HallProperty.update_properties(hall_id=instance.id, **properties)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True, url_path='property')
    def delete_property(self, requests, pk=None):
        hall = self.get_object()
        properties = requests.data.get('properties', None)
        if properties:
            HallProperty.delete_properties(hall_id=hall.id, **properties)
            return Response(status=status.HTTP_200_OK)

    @extend_schema(responses=OrderSerializer(many=True))
    @action(methods=['get'], detail=True, url_path='order-date')
    def ordered(self, request, pk=None):
        obj = self.get_object()
        approved_orders = obj.orders.prefetch_related('histories').filter(histories__status__order_status_name='approved')
        serializer = OrderSerializer(instance=approved_orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class HallFavoriteViewSet(ModelViewSet):
    queryset = HallFavorite.objects.all()
    serializer_class = HallFavoriteSerializer


class EventTypeViewSet(ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
