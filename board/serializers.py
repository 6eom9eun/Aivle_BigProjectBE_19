from rest_framework import serializers
from .models import Post, Comment, Image

class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    profile_image = serializers.ReadOnlyField(source='profile.image.url') # 이미지가 경로 url 이면 .url 붙여야 됨.
    image = serializers.ImageField(use_url=True, required=False) 
    
    class Meta:
        model = Comment
        fields = ['comment_id', 'user_id', 'username', 'profile_image', 'reply', 'created_at', 'comment', 'image']
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
    comments = CommentSerializer(many=True, required=False) 
    image = serializers.ImageField(use_url=True, required=False) 

    class Meta:
        model = Post
        fields = ['post_id', 'user_id', 'username', 'title', 'content', 'created_at', 'comments', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comments = Comment.objects.filter(reply=instance).prefetch_related('user__profile') # 댓글 사용자 프로필 미리 가져오기
        comments_data = CommentSerializer(comments, many=True).data
        representation['comments'] = comments_data
        return representation

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "image")
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'