from django.urls import path, include

from . import views
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post') # (게시글)
router.register('comments', CommentViewSet, basename='comment') # (댓글)

app_name = 'board'
urlpatterns = [
    path('', include(router.urls)),
]

"""
    from rest_framework import routers
    router = routers.SimpleRouter()

    from .views import PostViewSet

    router.register('posts', PostViewSet)
    
"""