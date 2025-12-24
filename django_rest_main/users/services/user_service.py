from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from users.models import User
from api.utils import send_email
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    ValidationError,
    PermissionDenied,
)
from django.contrib.auth import authenticate


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def verify_token(token: str, max_age: int = 60 * 60 * 24):
    signer = TimestampSigner()

    try:
        user_id = signer.unsign(token, max_age)
    except SignatureExpired:
        raise ValidationError("Token expired")
    except BadSignature:
        raise ValidationError("Invalid token")
    return user_id


def sign_token(user_id):
    signer = TimestampSigner()
    try:
        token = signer.sign(str(user_id))
    except Exception as e:
        raise ValidationError(e)
    return token


def find_user_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("User not found")
    return user


def find_one(email: str, all: bool = False):
    email = email.strip().lower()

    filters = {"email": email}

    if not all:
        filters["is_active"] = True

    return User.objects.filter(**filters).first()


class UserService:
    @staticmethod
    def register_user(data):
        email = data["email"]
        name = data["name"]
        password = data["password"]

        user = User.objects.create_user(email=email, name=name, password=password)
        token = sign_token(user.id)
        link = f"http://localhost:3000/verify-email?token={token}"
        email_body_plain = "Click Following Link to Verify Your Email " + link
        send_email(
            to_email=user.email,
            subject="Verify Your Email",
            plain_content=email_body_plain,
        )
        return user

    @staticmethod
    def verify_email(data):
        token = data["token"]
        user_id = verify_token(token)
        user = find_user_by_id(user_id)
        if user.is_active:
            raise PermissionDenied("Email already verified")
        user.is_active = True
        user.save()
        return user

    @staticmethod
    def resend_verify_email(data):
        email = data["email"]
        user = find_one(email, True)
        if user:
            if user.is_active:
                raise PermissionDenied("Email already verified")
            token = sign_token(user.id)
            link = f"http://localhost:3000/verify-email?token={token}"
            email_body_plain = "Click Following Link to Verify Your Email " + link
            send_email(
                to_email=user.email,
                subject="Verify Your Email",
                plain_content=email_body_plain,
            )
            return user
        raise NotFound("User not found")

    @staticmethod
    def login_user(data):
        email = data["email"]
        existing_user = find_one(email, True)

        if existing_user:
            if not existing_user.is_active:
                raise PermissionDenied("Email is not verified")

            password = data["password"]

            user = authenticate(email=email, password=password)
            if user is None:
                raise AuthenticationFailed("Invalid credentials")
            token = get_tokens_for_user(user)
            return token

        raise NotFound("User not found")

    @staticmethod
    def change_password(data, user):
        password = data["password"]
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def forgot_password(data):
        email = data["email"]
        user = find_one(email, True)
        if user:
            if not user.is_active:
                raise PermissionDenied("Email is not verified")
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            link = f"http://localhost:3000/reset-password/{uid}?token={token}"
            email_body_plain = "Click Following Link to Reset Your Password " + link
            send_email(
                to_email=user.email,
                subject="Reset Your Password",
                plain_content=email_body_plain,
            )
            return user
        raise NotFound("User not found")

    @staticmethod
    def reset_password(data):
        uid = data["uid"]
        token = data["token"]
        password = data["password"]
        user_id = smart_str(urlsafe_base64_decode(uid))
        user = find_user_by_id(user_id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError("Token is not Valid or Expired")
        user.set_password(password)
        user.save()
        return user
