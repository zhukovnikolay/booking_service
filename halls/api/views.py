import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .serializers import HallTypeSerializer, PropertySerializer, HallSerializer, HallFavoriteSerializer
from halls.models import HallType, Property, Hall, HallProperty, HallFavorite


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


class HallFavoriteViewSet(ModelViewSet):
    queryset = HallFavorite.objects.all()
    serializer_class = HallFavoriteSerializer
