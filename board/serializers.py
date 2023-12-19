from rest_framework import serializers
from .models import Post, Comment
  
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ('id', 'user', 'title', 'content', 'created_at')