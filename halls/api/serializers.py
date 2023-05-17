import json

from django.contrib.auth import get_user_model
from rest_framework import serializers


from halls.models import Hall, HallType, Property, HallProperty, HallMedia, HallFavorite, EventType

User = get_user_model()


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ['id', 'event_type_name']


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
        fields = ['id', 'hall', 'file', 'is_avatar']


class HallSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField(required=False,)
    media = serializers.SerializerMethodField(required=False,)
    avatar = serializers.SerializerMethodField(required=False,)
    recommendations = serializers.ListField(read_only=True,)

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
            'avatar',
            'media',
            'event_type',
            'recommendations',
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
        if self.context['request'].method in ['POST', 'PATCH', 'PUT']:
            hall_media = json.loads(self.context['request'].data.get('hall_media', '[]'))
        if self.context['request'].method == 'GET':
            hall_media = obj.files.filter(is_avatar=False)
        return serializer.to_representation(hall_media)

    def get_avatar(self, obj):
        serializer = HallMediaSerializer(many=False)
        if self.context['request'].method in ['POST', 'PATCH', 'PUT']:
            avatar = self.context['request'].data.get('avatar')
            if avatar is None:
                return None
            return json.loads(avatar)
        if self.context['request'].method == 'GET':
            avatar = obj.files.filter(is_avatar=True).first()
            if avatar is None:
                return None
        return serializer.to_representation(avatar)

    def create(self, validated_data):
        properties = json.loads(self.context['request'].data.get('properties', '[]'))
        hall_type = validated_data.pop('hall_type', None)
        event_type = validated_data.pop('event_type', None)
        hall_medias = validated_data.pop('media', None)
        avatar = validated_data.pop('avatar', None)

        hall = Hall.objects.create(**validated_data)
        if hall_type:
            hall.hall_type.set(hall_type)

        if event_type:
            hall.event_type.set(event_type)
        hall_properties = {values['property_name']: values['property_value'] for values in properties}
        HallProperty.insert_properties(hall_id=hall.id, **hall_properties)

        if hall_medias:
            for media in hall_medias:
                HallMedia.objects.create(hall=hall, file=media,)
        if avatar:
            HallMedia.objects.create(hall=hall, file=avatar, is_avatar=True)
        return hall

    def to_internal_value(self, data):
        internal_value = super(HallSerializer, self).to_internal_value(data)
        media = data.getlist('media')
        avatar = data.get('avatar')
        internal_value.update({'media': media})
        internal_value.update({'avatar': avatar})
        return internal_value


class HallFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())

    class Meta:
        model = HallFavorite
        fields = ['id', 'user', 'hall', ]
