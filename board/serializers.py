# board > serializers.py
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'image', 'reply', 'created_at', 'comment']
        read_only_fields = ['reply']
        
    def get_image(self, obj):
        profile = User.objects.get(username=obj.user.username).profile
        image_url = f'http://localhost:8000{profile.image.url}'
        return image_url
    
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username') # views.py에서 넘겨준 user의 username 값 받아옴
    class Meta:
        model = Post
        fields = ['post_id', 'user', 'title', 'created_at']

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Post
        fields = ['post_id', 'user', 'title', 'content', 'created_at', 'comments', 'image']
 
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "image")
