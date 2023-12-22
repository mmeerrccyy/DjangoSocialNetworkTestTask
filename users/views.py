from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from users.models import CustomUserModel
from users.serializers import UserRegisterSerializer, UserAuthSerializer


class LoginView(APIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUserModel.objects.get(email=serializer.validated_data["email"])
        if not user or not user.check_password(serializer.validated_data["password"]):
            raise APIException("Incorrect username or password!", status.HTTP_400_BAD_REQUEST)
        tokens = RefreshToken.for_user(user)
        user.last_request = timezone.now()
        user.save()
        return Response(self.serializer_class({
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens),
            "last_login": user.last_login,
            "last_request": user.last_request
        }).data)


class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        tokens = RefreshToken.for_user(new_user)
        new_user.last_request = timezone.now()
        new_user.save()
        return Response(UserAuthSerializer({
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens),
            "last_login": new_user.last_login,
            "last_request": new_user.last_request
        }).data)