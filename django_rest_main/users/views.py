from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.models import User
from users.services.user_service import UserService
from rest_framework.permissions import AllowAny
from .serializers import (
    UserChangePasswordSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserForgotPasswordSerializer,
    UserPasswordResetSerializer,
    UserVerifyEmailSerializer,
)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.register_user(serializer.validated_data)
        return Response(
            {"msg": "User Registered Successfully"},
            status=status.HTTP_201_CREATED,
        )

class UserVerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserVerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.verify_email(serializer.validated_data)
        return Response({"msg": "Email Verified Successfully"}, status=status.HTTP_200_OK)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = UserService.login_user(serializer.validated_data)
        return Response(
            {"token": token, "msg": "Login Successful"},
            status=status.HTTP_200_OK,
        )


class UserProfileView(APIView):
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset link send. Please check your Email"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Reset Successfully"}, status=status.HTTP_200_OK
        )
