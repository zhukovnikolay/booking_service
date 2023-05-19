import json

from django.db.models import Q
from django.utils.datetime_safe import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from orders.api.serializers import OrderSerializer
from orders.models import OrderHistory
from .serializers import HallTypeSerializer, PropertySerializer, HallSerializer, HallFavoriteSerializer, \
    EventTypeSerializer
from halls.models import HallType, Property, Hall, HallProperty, HallFavorite, EventType
from utils import recomender


class HallTypeViewSet(ModelViewSet):
    serializer_class = HallTypeSerializer
    queryset = HallType.objects.all()


class PropertyViewSet(ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()


class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

    def get_queryset(self):
        queryset = Hall.objects.all()
        price_from = self.request.query_params.get('price_from')
        price_till = self.request.query_params.get('price_till')
        area_from = self.request.query_params.get('area_from')
        area_till = self.request.query_params.get('area_till')
        capacity_from = self.request.query_params.get('capacity_from')
        capacity_till = self.request.query_params.get('capacity_till')
        event_type = self.request.query_params.get('event_type')
        hall_type = self.request.query_params.get('hall_type')
        filter_from = self.request.query_params.get('order_from')
        filter_till = self.request.query_params.get('order_till')
        if price_till:
            queryset = queryset.filter(price__lt=price_till)
        if price_from:
            queryset = queryset.filter(price__gt=price_from)
        if area_from:
            queryset = queryset.filter(area__gt=int(area_from))
        if area_till:
            queryset = queryset.filter(area__lt=area_till)
        if capacity_from:
            queryset = queryset.filter(capacity__gt=capacity_from)
        if capacity_till:
            queryset = queryset.filter(capacity__lt=capacity_till)
        if hall_type:
            queryset = queryset.filter_all_many_to_many('hall_type__id', *hall_type.split(','))
        if event_type:
            queryset = queryset.filter_all_many_to_many('event_type__id', *event_type.split(','))
        if filter_from and filter_till:
            filter_from = datetime.strptime(filter_from, '%Y-%m-%d')
            filter_till = datetime.strptime(filter_till, '%Y-%m-%d')
            halls_with_order = OrderHistory.objects.filter(status__order_status_name='approved',
                                                           end_date__isnull=True).filter(
                (Q(order__order_till__lt=filter_till) & Q(order__order_till__gt=filter_from)) |
                (Q(order__order_from__lt=filter_till) & Q(order__order_till__gt=filter_till))
            ).values_list('order__hall_id', flat=True)
            queryset = queryset.exclude(id__in=halls_with_order)
        return queryset

    @extend_schema(parameters=[
        OpenApiParameter(name='price_till', type=OpenApiTypes.DECIMAL, required=False),
        OpenApiParameter(name='price_from', type=OpenApiTypes.DECIMAL, required=False),
        OpenApiParameter(name='area_from', type=OpenApiTypes.DECIMAL, required=False),
        OpenApiParameter(name='area_till', type=OpenApiTypes.DECIMAL, required=False),
        OpenApiParameter(name='capacity_from', type=OpenApiTypes.INT, required=False),
        OpenApiParameter(name='capacity_till', type=OpenApiTypes.INT, required=False),
        OpenApiParameter(name='hall_type', type=OpenApiTypes.STR, required=False, description='comma separated string with hall type ID'),
        OpenApiParameter(name='event_type', type=OpenApiTypes.STR, required=False, description='comma separated string with event type ID'),
        OpenApiParameter(name='order_from', type=OpenApiTypes.DATE, required=False),
        OpenApiParameter(name='order_from', type=OpenApiTypes.DATE, required=False),
    ])
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        hall = self.get_object()
        hall.increase_view_count()
        # ToDo need to store data about all halls in cache
        data = recomender.load_data()
        recommendations = recomender.recommender(hall.id, data)
        serializer = HallSerializer(hall, many=False, context=self.get_serializer_context())
        serializer_data = serializer.data
        serializer_data.update({'recommendations': recommendations})
        can_make_comment = False
        if user.is_authenticated:
            user_orders = user.orders.filter(hall=hall)
            if user_orders.count() > 0:
                is_order_finished = user.orders.prefetch_related('histories').filter(
                    hall=hall,
                    histories__status__order_status_name='finished',
                    histories__end_date__isnull=True
                ).count()
                if is_order_finished > 0:
                    can_make_comment = True
        serializer_data.update({'canComment': can_make_comment})
        return Response(serializer_data, status=status.HTTP_200_OK)

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
            properties = {hall_property['property_name']: hall_property['property_value'] for hall_property in
                          properties}
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
        approved_orders = obj.orders.prefetch_related('histories').filter(
            histories__status__order_status_name='approved')
        serializer = OrderSerializer(instance=approved_orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class HallFavoriteViewSet(ModelViewSet):
    queryset = HallFavorite.objects.all()
    serializer_class = HallFavoriteSerializer


class EventTypeViewSet(ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
