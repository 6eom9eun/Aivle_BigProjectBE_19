# board > serializers.py
from rest_framework import serializers
from .models import Post, Comment
          
class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    image = serializers.ReadOnlyField(source='profile.image.url') # 이미지가 경로 url 이면 .url 붙여야 됨.

    class Meta:
        model = Comment
        fields = ['user_id', 'username', 'comment_id', 'image', 'reply', 'created_at', 'comment']
        read_only_fields = ['reply']
        
class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source = 'user.username') # views.py에서 넘겨준 user의 username 값 받아옴
    class Meta:
        model = Post
        fields = ['username', 'user_id', 'post_id', 'title', 'created_at', 'image']

class PostDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Post
        fields = ['user_id', 'username', 'post_id','title', 'content', 'created_at', 'comments', 'image']
 
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "image")

# 이미지 업로드 시리얼라이저
class ImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField()) # 이미지 여러장