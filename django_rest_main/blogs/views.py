from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from blogs.serializers import BlogSerializer, CommentSerializer
from api.paginations import CustomPagination
from .filters import BlogFilter
from blogs.models import Blog, Comment


class BlogsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = CustomPagination
    # filterset_fields = ['id', 'blog_title']  # global filtering
    filterset_class = BlogFilter  # custom filtering


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"


class CommentsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
