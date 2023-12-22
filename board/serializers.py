# board > serializers.py
from rest_framework import serializers
from .models import Post, Comment
          
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    # reply = PostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'reply', 'created_at', 'comment']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username') # views.py에서 넘겨준 user의 username 값 받아옴
    # comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)  # 게시글에 달린 댓글 갯수
    class Meta:
        model = Post
        fields = ['post_id', 'user', 'title', 'content', 'created_at', 'comments', 'comments_count']
        
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")
