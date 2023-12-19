from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import SignupSerializer, LoginSerializer

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # 데이터 유효성 확인
        token = serializer.validated_data # validate()의 리턴값인 token을 받아오기, 유효성 검사
        return Response({"token": token.key}, status=status.HTTP_200_OK)