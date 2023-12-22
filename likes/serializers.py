from rest_framework import serializers


class LikeStatsSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
