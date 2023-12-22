# board > views.py
from django.urls import is_valid_path
from board.serializers import PostSerializer, PostCreateSerializer, CommentSerializer
from .permissions import CustomReadOnly
from .models import Post, Comment

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import get_object_or_404, get_list_or_404

# Post의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at') # 생성일자기준으로 내림차순
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, CustomReadOnly] # 비인증 요청에 대해서는 읽기만 허용
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'published_at']
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
        
# (댓글) Comment 보여주기, 수정하기, 삭제하기 모두 가능
class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, CustomReadOnly]
    # queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Comment.objects.filter(reply__post_id=post_pk).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, reply_id=self.kwargs.get("post_pk"))

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