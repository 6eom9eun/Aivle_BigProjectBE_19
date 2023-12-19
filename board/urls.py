from django.urls import path, include

from . import views
from .views import PostViewSet

"""
    from rest_framework import routers
    router = routers.SimpleRouter()

    from .views import PostViewSet

    router.register('posts', PostViewSet)
    
"""

# Post 목록 보여주기
post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Post detail 보여주기 + 수정 + 삭제
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

app_name = 'board'
urlpatterns = [
    path('', post_list),
    path('<int:pk>/', post_detail),
]