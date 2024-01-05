from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import CustomReadOnly, IsOwnerOrReadOnly
from .models import Post, Comment, Image
from accounts.models import Profile
from .serializers import PostSerializer, PostCreateSerializer, PostDetailSerializer, CommentSerializer

# Post의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class PostViewSet(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, CustomReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'published_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PostDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().order_by('-created_at') # 생성일자기준으로 내림차순
    serializer_class = PostDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] # 비인증 요청에 대해서는 읽기만 허용
    lookup_field = 'post_id'
    partial_update = True  # 부분 업데이트 허용 설정
        
# (댓글) Comment 목록 보여주기
class CommentViewSet(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'post_id'
    
    def get_queryset(self):
        post_pk = self.kwargs.get("post_id")
        return Comment.objects.filter(reply__post_id=post_pk).order_by('-created_at')

    def perform_create(self, serializer):
        try:
            post_pk = self.kwargs.get("post_id")
            post = get_object_or_404(Post, pk=post_pk)
            serializer.save(user=self.request.user, reply=post)
            user_profile = Profile.objects.get(user=self.request.user)
            serializer.save(profile=user_profile)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# (댓글) Comment 조회, 수정, 삭제     
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    
# 이미지 업로드 뷰
class ImageUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            image_file = request.FILES.get('image')
            if image_file:
                new_image = Image.objects.create(image=image_file)
                image_url = new_image.image.url
                response_data = {
                    'image_id': new_image.id,
                    'image_url': image_url
                }
                return JsonResponse(response_data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': '이미지 파일이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, image_id, *args, **kwargs):
        try:
            image_instance = Image.objects.get(pk=image_id)
        except Image.DoesNotExist:
            return JsonResponse({'error': '이미지를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        image_instance.delete()
        return JsonResponse({'message': '성공적으로 삭제 완료 !'}, status=status.HTTP_204_NO_CONTENT)