from rest_framework import serializers

from users.models import CustomUserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ["username", "public_id"]
        extra_kwargs = {"username": {"required": False}}


class UserRegisterSerializer(serializers.Serializer):

    email = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    def create(self, validated_data):
        return CustomUserModel.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class UserAuthSerializer(serializers.Serializer):

    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    last_request = serializers.DateTimeField(read_only=True)
