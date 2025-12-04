from django.urls import path
from . import views

urlpatterns = [
    path("blogs/", views.BlogsView.as_view()),
    path("blogs/<int:pk>/", views.BlogDetailView.as_view()),
    path("comments/", views.CommentsView.as_view()),
    path("comments/<int:pk>/", views.CommentDetailView.as_view()),
]