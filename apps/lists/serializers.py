from rest_framework import serializers

from apps.lists.models import List


class ListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "slug"]

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m.%d.%Y, %H:%M:%S")
        return formatted_date
