# board > urls.py
from django.urls import path, include

from . import views
from .views import PostViewSet, PostDetailViewSet, CommentViewSet

app_name = 'board'
urlpatterns = [
    path('', PostViewSet.as_view(), name = "post-list"),
    path('<int:post_id>/', PostDetailViewSet.as_view(), name="post-detail"),
    path("<int:post_id>/comments/", CommentViewSet.as_view({"post": "create", "get": "list"}), name="comment-detail"),
]