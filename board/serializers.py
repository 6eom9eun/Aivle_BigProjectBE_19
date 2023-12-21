from rest_framework import serializers
from .models import Post, Comment
  
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username') # views.py에서 넘겨준 user의 username 값 받아옴
    class Meta:
        model = Post
        fields = ('post_id', 'user', 'title', 'content', 'created_at')
        
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'reply', 'created_at', 'comment']