from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
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

# 유저 정보 업데이트 뷰
class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)