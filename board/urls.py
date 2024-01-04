# board > urls.py
from django.urls import path, include

from .views import PostViewSet, PostDetailViewSet, CommentViewSet, CommentDetailView, image_upload

app_name = 'board'
urlpatterns = [
    path('', PostViewSet.as_view(), name = "post-list"),
    path('image-upload/', image_upload, name='image-upload'),
    path('<int:post_id>/', PostDetailViewSet.as_view(), name="post-detail"),
    path("<int:post_id>/comments/", CommentViewSet.as_view(), name="comment-list"),
    path("<int:post_id>/comments/<int:comment_id>/", CommentDetailView.as_view(), name="comment-detail"),
]