from django.urls import path, include
from employees.urls import employeeRouter

urlpatterns = [
    # Auth endpoints
    path("auth/", include("users.urls")),
    
    # Student endpoints
    path("students/", include("students.urls")),
    
    # Employee endpoints
    path("employees/", include("employees.urls")),
    # path("", include(employeeRouter.urls)),
    
    # Blog endpoints
    path("", include("blogs.urls")),
]
