from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    avatar = serializers.ReadOnlyField(source="profile.avatar.url")

    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "date_joined", "avatar"]


class CreateUserSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "password"]
