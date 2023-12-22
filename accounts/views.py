from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.generics import UpdateAPIView

from .serializers import *

# 회원가입 뷰 : 생성 기능 -> CreateAPIView
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

# 로그인 뷰 : 모델 영향 X -> GenericAPIView 상속
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # Token
        return Response({"token": token.key}, status=status.HTTP_200_OK)

# 유저 정보 뷰    
class UserDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            queryset = Profile.objects.all()
            obj = queryset.get(user=self.request.user)
            self.check_object_permissions(self.request, obj)
            return obj
        except Profile.DoesNotExist:
            return Response({'detail': '프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        user_serializer = UserDetailSerializer(instance=request.user)
        profile_serializer = self.get_serializer(self.get_object())

        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data,
        }, status=status.HTTP_200_OK)
        
# 유저 정보 업데이트 뷰
class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    authentication_classes = [TokenAuthentication] # 토큰 인증
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object() # 사용자 객체 가져오기, 유효성 검사
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)