from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User, Interest
from halls.api.serializers import HallFavoriteSerializer


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ['id', 'interest_name']


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
            'interest'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    interest = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True, required=False)
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
            'interest',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        interest = validated_data.pop('interest')
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
        if interest:
            user.interest.set(interest)
        return user
