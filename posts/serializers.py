from rest_framework import serializers

from posts.models import PostModel
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    user_public_id = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    likes = serializers.IntegerField(read_only=True, source="likemodel_set.count")

    class Meta:
        model = PostModel
        fields = ["id", "text", "created_at", "user", "user_public_id", "likes"]

    def create(self, validated_data):
        return PostModel.objects.create(user_id=self.context["user"].id, **validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
