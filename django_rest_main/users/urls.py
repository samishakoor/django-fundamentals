from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
)

urlpatterns = [
    # Public endpoints
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
    # Protected endpoints
    path("change-password/", UserChangePasswordView.as_view(), name="change-password"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
