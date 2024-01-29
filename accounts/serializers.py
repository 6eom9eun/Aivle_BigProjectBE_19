from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # 장고 pw 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 이메일 중복 방지 검증

from django.contrib.auth import authenticate # Django의 기본 authenticate 함수 -> 설정한 TokenAuth 방식으로 유저를 인증.
from django.contrib.auth.hashers import check_password
from django.utils import timezone # 마지막 로그인 시간 체크를 위함
from django.db import connection
from django.db.models import Prefetch

import re

from .models import *
from rank.models import Ranking

# 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, error_messages={'blank': "이 필드는 필수 입력 정보입니다."})
    last_name = serializers.CharField(required=True, error_messages={'blank': "이 필드는 필수 입력 정보입니다."})
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="이미 등록된 이메일입니다.")],
        error_messages={'blank': "이 필드는 필수 입력 정보입니다.", 'invalid': '유효한 이메일 주소를 입력하십시오.'}
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="이미 사용 중인 사용자 아이디입니다.")],
        error_messages={'blank': "이 필드는 필수 입력 정보입니다."}
    )
    password = serializers.CharField(write_only=True, required=True, error_messages={'blank': "이 필드는 필수 입력 정보입니다."})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password',)

    def validate(self, data):
        required_fields = ['first_name', 'last_name', 'email', 'username', 'password']

        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: "이 필드는 필수 입력 정보입니다."})

        return data
    
    def validate_email(self, value):
        email_regex = r"^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$"
        if not re.match(email_regex, value):
            raise serializers.ValidationError({"email": "이메일 형식이 올바르지 않습니다."})
        return value

    def validate_password(self, value):
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+{}|;':\",./<>?`~[\]\\\-]{8,}$"
        if not re.match(password_regex, value):
            raise serializers.ValidationError({"password": "비밀번호는 최소 8자리이며, 알파벳과 숫자를 포함해야 합니다."})
        return value

    def create(self, validated_data):    
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

    
# 로그인 시리얼라이저 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True) # write_only=True : 클라이언트 -> 서버 역직렬화 가능, 서버 -> 클라이언트 직렬화 X
    last_login = serializers.DateTimeField(read_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        print(user.is_authenticated)
        print(f"user: {user}")
        if user:
            token = Token.objects.get(user=user)
            print(f"token: {token.key}")
            user.last_login = timezone.now()
            user.save()
            return token
        raise serializers.ValidationError(
            {"error": "제공된 자격 증명으로 로그인할 수 없습니다."}
        )

# 유저 정보 시리얼라이저
class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'last_login', 'date_joined')

# 프로필 시리얼라이저
class ProfileSerializer(serializers.ModelSerializer):
    user_level = serializers.IntegerField(source='user.ranking.user_level', read_only=True)
    
    class Meta:
        model = Profile
        fields = ('introduction', 'image', 'user_level')

    def to_representation(self, instance):
        # select_related를 사용하여 N+1 문제 해결
        queryset = Profile.objects.select_related('user__ranking')
        instance = queryset.get(pk=instance.pk)
        return super().to_representation(instance)

        
# 유저 정보 수정 시리얼라이저
class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'old_password',)
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password', None)

        if old_password and not check_password(old_password, instance.password):
            raise serializers.ValidationError({'old_password': '이전 비밀번호가 올바르지 않습니다.'})

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        new_password = validated_data.get('password')
        if new_password:
            instance.set_password(new_password)

        instance.save()

        return instance
    
# 프로필 수정 시리얼라이저 
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('introduction', 'image',)

    def update(self, instance, validated_data):
        instance.introduction = validated_data.get('introduction', instance.introduction)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance
    
    



