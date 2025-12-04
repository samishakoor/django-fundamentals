from django.urls import path
from . import views

urlpatterns = [
    path('', views.studentsView),
    path('<int:id>/', views.studentDetailView),
]