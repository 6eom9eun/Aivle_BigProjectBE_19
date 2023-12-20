from django.urls import is_valid_path
from board.serializers import PostSerializer, PostCreateSerializer
from .permissions import CustomReadOnly
from .models import Post, Comment

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets

from django.shortcuts import get_object_or_404, get_list_or_404

"""
    post_id : 글 번호
    user : 작성자
    title: 제목
    content: 내용
    created_at: 작성일
    published_at: 배포일
"""
# Post의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at') # 생성일자기준으로 내림차순
    serializer_class = PostSerializer
    permission_classes = [CustomReadOnly] # 읽기전용권한
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'published_at']
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

"""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend 
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from .permissions import CustomReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    permission_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'published_at']
    
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return PostSerializer
        return PostCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
"""