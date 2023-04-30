import json

from django.contrib.auth import get_user_model
from rest_framework import serializers

from halls.models import Hall, HallType, Property, HallProperty
from orders.api.serializers import OrderSerializer


User = get_user_model()

class HallTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HallType
        fields = ['id', 'type_name']


class PropertySerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(many=False, queryset=HallType.objects.all(), allow_null=False)

    class Meta:
        model = Property
        fields = ['id', 'property_name', 'property_type', 'type']


class HallPropertySerializer(serializers.Serializer):
    property_name = serializers.CharField()
    property_value = serializers.CharField()

    class Mete:
        fields = ['property_name', 'property_fields']


class HallSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Hall
        fields = ['id', 'name', 'descriptions', 'user', 'hall_type', 'view_count', 'properties', 'approved_order_date']

    def get_properties(self, obj):
        serializer = HallPropertySerializer(many=True)
        if self.context['request'].method in ['POST', 'PATCH', 'PUT']:
            properties = json.loads(self.context['request'].data.get('properties', '[]'))
        if self.context['request'].method == 'GET':
            properties = HallProperty.get_hall_properties(hall_id=obj.id)
        return serializer.to_representation(properties)

    def create(self, validated_data):
        properties = json.loads(self.context['request'].data.get('properties', '[]'))
        hall_type = validated_data.pop('hall_type', None)
        hall = Hall.objects.create(**validated_data)
        if hall_type:
            hall.hall_type.set(hall_type)
        hall_properties = {values['property_name']: values['property_value'] for values in properties}
        HallProperty.insert_properties(hall_id=hall.id, **hall_properties)
        return hall
