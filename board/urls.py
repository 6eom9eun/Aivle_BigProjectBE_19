# board > urls.py
from django.urls import path
from .views import PostViewSet, PostDetailViewSet, CommentViewSet, CommentDetailView, ImageUploadView

app_name = 'board'
urlpatterns = [
    path('', PostViewSet.as_view(), name = "post-list"),
    path('image-upload/', ImageUploadView.as_view(), name='image-upload'),
    path('image-delete/<int:image_id>/', ImageUploadView.as_view(), name='image-delete'),
    path('<int:post_id>/', PostDetailViewSet.as_view(), name="post-detail"),
    path("<int:post_id>/comments/", CommentViewSet.as_view(), name="comment-list"),
    path("<int:post_id>/comments/<int:comment_id>/", CommentDetailView.as_view(), name="comment-detail"),
]