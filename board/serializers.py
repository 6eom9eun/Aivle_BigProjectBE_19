from rest_framework import serializers
from .models import Post, Comment, Image

class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    image = serializers.ReadOnlyField(source='profile.image.url') # 이미지가 경로 url 이면 .url 붙여야 됨.

    class Meta:
        model = Comment
        fields = ['comment_id', 'user_id', 'username', 'image', 'reply', 'created_at', 'comment']
        read_only_fields = ['reply']
        
class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source = 'user.id') # views.py에서 넘겨준 user의 username 값 받아옴
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Post
        fields = ['post_id', 'user_id', 'username', 'title', 'created_at', 'image']

class PostDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Post
        fields = ['post_id', 'user_id', 'username', 'title', 'content', 'created_at', 'comments', 'image']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "image")
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        