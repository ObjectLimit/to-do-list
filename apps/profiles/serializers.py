from rest_framework import serializers

from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    full_name = serializers.ReadOnlyField(source="user.get_full_name")
    email = serializers.EmailField(source="user.email")
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "username", "email", "full_name", "avatar"]

    def get_avatar(self, obj: Profile) -> str | None:
        try:
            return obj.avatar.url
        except AttributeError:
            return None


class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]
