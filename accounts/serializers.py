from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # 장고 pw 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 이메일 중복 방지 검증

from django.contrib.auth import authenticate # Django의 기본 authenticate 함수 -> 설정한 TokenAuth 방식으로 유저를 인증.

from django.utils import timezone # 마지막 로그인 시간 체크를 위함

# 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 이메일 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호에 대한 검증
    )
    password2 = serializers.CharField( # 비밀번호 확인을 위한 필드
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data): # password과 password2의 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호 일치하지 않음."})
        return data

    def create(self, validated_data):
        # CREATE 요청에 대해 create 메서드를 오버라이딩, 유저를 생성하고 토큰도 생성하게 해준다.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True) # write_only=True : 클라이언트 -> 서버 역직렬화 가능, 서버 -> 클라이언트 직렬화 X
    last_login = serializers.DateTimeField(read_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) # 유저의 토큰을 불러오기
            user.last_login = timezone.now() # 마지막 로그인 시간 저장
            user.save()
            return token
        raise serializers.ValidationError( # 가입된 유저 X
            {"error": "제공된 자격 증명으로 로그인할 수 없습니다."}
        )
