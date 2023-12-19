from django.urls import is_valid_path
from board.serializers import PostSerializer
from .models import Post, Comment

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import get_object_or_404, get_list_or_404

"""
    post_id : 글 번호
    user : 작성자
    title: 제목
    content: 내용
    created_at: 작성일
    published_at: 배포일
"""
@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        # posts = post.objects.all()
        posts = get_list_or_404(Post)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)