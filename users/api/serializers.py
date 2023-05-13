from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from halls.api.serializers import HallFavoriteSerializer


class UserSerializer(serializers.ModelSerializer):
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
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'user_agreement',
            'offer_agreement',
            'show_phone_number',
            'phone_number',
        ]

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            return serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            user_agreement=validated_data['user_agreement'],
            offer_agreement=validated_data['offer_agreement'],
            show_phone_number=validated_data['show_phone_number'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(password1)
        print(user.username)
        return user
