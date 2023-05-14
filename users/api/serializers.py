from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from halls.api.serializers import HallFavoriteSerializer


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'user_agreement',
            'offer_agreement',
            'show_phone_number',
            'phone_number',
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):
    favorites = HallFavoriteSerializer(many=True, required=False)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'user_agreement',
            'offer_agreement',
            'show_phone_number',
            'phone_number',
            'favorites',
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'user_agreement',
            'offer_agreement',
            'show_phone_number',
            'phone_number',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            user_agreement=validated_data['user_agreement'],
            offer_agreement=validated_data['offer_agreement'],
            show_phone_number=validated_data['show_phone_number'],
            phone_number=validated_data['phone_number'],
            password=password,
        )
        return user
