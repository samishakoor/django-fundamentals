from django.urls import path
from .views import LogoutView, RegisterView, LoginView

urlpatterns = [
    # Public endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Protected endpoints
    path('logout/', LogoutView.as_view(), name='logout'),
]
