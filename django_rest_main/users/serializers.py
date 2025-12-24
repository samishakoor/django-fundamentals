from .models import User
from rest_framework import serializers


def confirm_password(password, confirm_password):
    if password != confirm_password:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return password


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "name", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("confirm_password")
        confirm_password(password, password2)
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserVerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=False, allow_null=False, write_only=True)

    class Meta:
        fields = ["token"]


class UserResendVerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True)

    class Meta:
        fields = ["email"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("confirm_password")
        confirm_password(password, password2)
        return attrs


class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True)

    class Meta:
        fields = ["email"]


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("confirm_password")
        confirm_password(password, password2)

        uid = self.context.get("uid", "")
        token = self.context.get("token", "")

        attrs["uid"] = uid
        attrs["token"] = token
        return attrs
