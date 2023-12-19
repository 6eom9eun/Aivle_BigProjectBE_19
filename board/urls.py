from django.urls import path

from . import views
from .views import PostViewSet

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