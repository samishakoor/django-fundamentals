from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

employeeRouter = DefaultRouter()
employeeRouter.register("employees", views.EmployeeViewset, basename="employeedirectories")

urlpatterns = [
    path('', views.EmployeeList.as_view()),
    path('<int:id>/', views.EmployeeDetail.as_view()),
]