import json

from django.contrib.auth import get_user_model
from rest_framework import serializers


from halls.models import Hall, HallType, Property, HallProperty, HallMedia, HallFavorite

User = get_user_model()


class HallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallType
        fields = ['id', 'type_name']


class PropertySerializer(serializers.ModelSerializer):
    hall_type = serializers.PrimaryKeyRelatedField(many=False, queryset=HallType.objects.all(), allow_null=False)

    class Meta:
        model = Property
        fields = ['id', 'property_name', 'property_type', 'hall_type']


class HallPropertySerializer(serializers.Serializer):
    property_name = serializers.CharField()
    property_value = serializers.CharField()

    class Mete:
        fields = ['property_name', 'property_fields']


class HallMediaSerializer(serializers.ModelSerializer):
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all(), required=False)
    file = serializers.ImageField(use_url=True)

    class Meta:
        model = HallMedia
        fields = ['id', 'hall', 'file']


class HallSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField(required=False)
    media = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Hall
        fields = [
            'id',
            'name',
            'descriptions',
            'owner',
            'hall_type',
            'view_count',
            'area',
            'capacity',
            'rating',
            'address',
            'price',
            'longitude',
            'latitude',
            'condition',
            'phone',
            'site',
            'vk',
            'telegram',
            'whatsapp',
            'properties',
            'approved_order_date',
            'media',
        ]

    def get_properties(self, obj):
        serializer = HallPropertySerializer(many=True)
        if self.context['request'].method in ['POST', 'PATCH', 'PUT']:
            properties = json.loads(self.context['request'].data.get('properties', '[]'))
        if self.context['request'].method == 'GET':
            properties = HallProperty.get_hall_properties(hall_id=obj.id)
        return serializer.to_representation(properties)

    def get_media(self, obj):
        serializer = HallMediaSerializer(many=True)
        print(self.context['request'].data)
        if self.context['request'].method in ['POST', 'PATCH', 'PUT']:
            hall_media = json.loads(self.context['request'].data.get('hall_media', '[]'))
        if self.context['request'].method == 'GET':
            hall_media = obj.files.all()
        return serializer.to_representation(hall_media)

    def create(self, validated_data):
        print(validated_data)
        properties = json.loads(self.context['request'].data.get('properties', '[]'))
        hall_type = validated_data.pop('hall_type', None)
        hall_medias = validated_data.pop('media', None)

        hall = Hall.objects.create(**validated_data)
        if hall_type:
            hall.hall_type.set(hall_type)
        hall_properties = {values['property_name']: values['property_value'] for values in properties}
        HallProperty.insert_properties(hall_id=hall.id, **hall_properties)

        if hall_medias:
            for media in hall_medias:
                HallMedia.objects.create(hall=hall, file=media)
        return hall

    def to_internal_value(self, data):
        internal_value = super(HallSerializer, self).to_internal_value(data)
        media = data.getlist('media')
        internal_value.update({'media': media})
        return internal_value


class HallFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())

    class Meta:
        model = HallFavorite
        fields = ['id', 'user', 'hall',]
