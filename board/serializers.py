# board > serializers.py
from rest_framework import serializers
from .models import Post, Comment
          
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    image = serializers.ReadOnlyField(source = 'profile.image')
    # reply = PostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'image', 'reply', 'created_at', 'comment']

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
