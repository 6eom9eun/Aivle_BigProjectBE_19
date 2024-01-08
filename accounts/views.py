from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from json.decoder import JSONDecodeError
from pathlib import Path
import requests
import json

from .serializers import *
from accounts.models import User

from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from rest_framework.permissions import AllowAny
from allauth.account.adapter import get_adapter
from django.shortcuts import redirect
from .serializers import *
from accounts.models import User
from django.db import IntegrityError, transaction
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.authtoken.models import Token

from django.conf import settings


import json
from json.decoder import JSONDecodeError
from pathlib import Path
import os


# --------- 소셜 로그인 api 주소 ----------
SECRET_BASE_DIR = Path(__file__).resolve().parent.parent
with open(SECRET_BASE_DIR/'secrets.json') as f:
    secrets = json.loads(f.read())
    # SECURITY WARNING: keep the secret key used in production secret!
KAKAO_REST_API_KEY = secrets['KAKAO_REST_API_KEY']
KAKAO_SECRET_KEY = secrets['KAKAO_SECRET_KEY']
KAKAO_REDIRECT_URI = secrets['KAKAO_REDIRECT_URI']
NAVER_REDIRECT_URI = secrets['NAVER_REDIRECT_URI']
BASE_URL = "http://127.0.0.1:8000/"

# ----------------------------------------

# 회원가입 뷰 : 생성 기능 -> CreateAPIView
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

# 로그인 뷰 : 모델 영향 X -> GenericAPIView 상속
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({'detail': '유효성 검사 실패', 'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data  # Token
        return Response({"token": token.key}, status=status.HTTP_200_OK)

# 유저 정보 뷰    
class UserDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user
    def get(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(self.get_object())

        return Response({
            'user': user_serializer.data,
        }, status=status.HTTP_200_OK)
        
# 유저 업데이트 뷰
class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # 부분적 업데이트 X => PUT
        instance = self.get_object()  # 사용자 객체 가져오기, 유효성 검사
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 사용자 정보와 프로필 정보 함께 업데이트
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
# 프로필 업데이트 뷰
class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 프로필을 현재 로그인한 사용자의 것으로 가져옵니다.
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # 부분적 업데이트 X => PUT
        instance = self.get_object()  # 프로필 객체 가져오기, 유효성 검사
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 프로필 정보 업데이트
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# 프로필 디테일   
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            queryset = Profile.objects.all()
            obj = queryset.get(user=self.request.user)
            self.check_object_permissions(self.request, obj)
            return obj
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            profile_serializer = self.get_serializer(self.get_object())
            return Response({'profile': profile_serializer.data}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'detail': '프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 다른 사용자 프로필 확인
class OtherUserProfileView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            user_id = self.kwargs.get('user_id')
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)
            self.check_object_permissions(self.request, profile)
            return profile
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            profile_serializer = self.get_serializer(self.get_object())
            return Response({'profile': profile_serializer.data}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'detail': '프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# KAKAO_REST_API_KEY = secrets['KAKAO_REST_API_KEY']
# KAKAO_SECRET_KEY = secrets['KAKAO_SECRET_KEY']
# KAKAO_REDIRECT_URI = secrets['KAKAO_REDIRECT_URI']

# ---------- 카카오 로그인 ---------------

@api_view(["GET"])
@permission_classes([AllowAny])

def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
    )

def kakao_callback(request):
    code = request.GET.get("code")
    print(f"code : {code}")
    
    # ---- Access Token Request ----
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&code={code}"
    )
    token_req_json = token_req.json()
    # print(f"Access Token 요청 결과: {token_req_json}")
    error = token_req_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(f"Failed to decode JSON: {error}", '{"error": "your_error_message"}', 0)

    access_token = token_req_json.get("access_token")
    print(f"access_token : {access_token}")
    
    # ---- Email Request ----
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    # print(f"Kakao Profile 요청 결과: {profile_json}")
    error = profile_json.get("error", None)
    if error is not None:
        raise JSONDecodeError("Failed to decode JSON", '{"error": "your_error_message"}', 0)

    kakao_account = profile_json.get("kakao_account")
    # kakao_account에서 이메일 외에 카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    # print(kakao_account)
    email = kakao_account.get("email", None)
    profile = kakao_account.get("profile")
    nickname = profile.get("nickname")
    profile_image = profile.get("thumbnail_image_url")
    # print(email)
    
    # ---- Signup or Signin Request ----
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        # 이메일은 있는데 카카오 유저가 아닌경우 = 일반회원인 경우
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not kakao social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        if social_user.provider != "kakao":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # 기존에 kakao로 가입된 유저
        print("===== 기존 Kakao 유저 로그인 =====")
        data = {"access_token": access_token, "code": code}
        # print(data)
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        
        if accept_status != 200:
            print(f"Accept 응답 상태 코드: {accept.status_code}")
            # print(f"data : {data}")
            return JsonResponse({"err_msg": "failed to signin_registered user."}, status=accept_status)
        accept_json = accept.json()
        # print(f"기존 Kakao 가입 유저 GET: {accept_json}")
        # accept_json.pop('user', None)
        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        cookie_max_age = 3600 * 24 * 14 # 14 days
        refresh_token = refresh_token[token_index+1]
        
        user = User.objects.get(username = accept_json['user']['username'])
        token = Token.objects.get(user = user)
        token_value = token.key
        accept_json['token'] = token_value
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie
    
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        cookie_max_age = 3600 * 24 * 14 # 로그인한 상태를 14일 동안 유지
        # print(email)
        data = {"access_token": access_token, "code": code}
        # print(data) 
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        
        print("===== 신규 Kakao 가입 =====")
    
        if accept_status != 200:
            print(f"Failed to signup_new user. Status code: {accept_status}")
            return JsonResponse({"err_msg": "failed to signup_new user"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴

        accept_json = accept.json()

        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        refresh_token = refresh_token[token_index+1]
        
        user = User.objects.get(username = accept_json['user']['username'])
        user.first_name = accept_json['user']['username'][1:]
        user.last_name = accept_json['user']['username'][:1]
        user.username = accept_json['user']['email'].split('@')[0]
        token = Token.objects.get_or_create(user = user)
        user.save()
        
        token = Token.objects.get(user = user)
        token_value = token.key
        accept_json['token'] = token_value
        
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie
    
    except JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        raise
    
    except User.MultipleObjectsReturned as e:
        print(f"MultipleObjectsReturned: {e}")
        return JsonResponse(
            {"err_msg": "MultipleObjectsReturned. Check logs for details."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    except:
        return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_REDIRECT_URI
    

#------------------naver-------------------------#
from rest_framework.views import APIView
from allauth.socialaccount.providers.naver import views as naver_view

# main domain(http://127.0.0.1:8000)
client_id = secrets['NAVER_CLIENT_ID']
state = secrets['STATE']
client_secret = secrets['NAVER_CLIENT_SECRET']

# 네이버 로그인 창
def naver_login(request):
    client_id = secrets['NAVER_CLIENT_ID']
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={NAVER_REDIRECT_URI}")

def naver_callback(request):
    client_id = secrets['NAVER_CLIENT_ID']
    client_secret = secrets['NAVER_CLIENT_SECRET']
    code = request.GET.get("code")
    state_string = request.GET.get("state")
    print("CODE : "+ code)
    print("STATE : "+ state_string)

    # code로 access token 요청
    token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state_string}")
    print("토큰 요청 상태 코드:", token_request.status_code)
    print("토큰 요청 내용:", token_request.content)
    token_response_json = token_request.json()

    error = token_response_json.get("error", None)
    if error is not None:
        print("네이버 API 오류:", error)
        raise Exception("네이버 API 오류: " + error)

    access_token = token_response_json.get("access_token")

    # access token으로 네이버 프로필 요청
    profile_request = requests.post(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print("프로필 요청 상태 코드:", profile_request.status_code)
    print("프로필 요청 내용:", profile_request.content)
    
    profile_json = profile_request.json()
    email = profile_json.get("response").get("email")

    if email is None:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 naver이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'naver':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 naver로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/naver/login/finish/", data=data)
        accept_status = accept.status_code

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        
        accept_json = accept.json()
        user = User.objects.get(email = profile_json.get("response").get("email"))
        token = Token.objects.get(user = user)
        token_value = token.key
        accept_json['token'] = token_value
        return JsonResponse(accept_json)
    
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/naver/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()

        user = User.objects.get(email = profile_json.get("response").get("email"))
        user.first_name = profile_json.get("response").get("name")[1:]
        user.last_name = profile_json.get("response").get("name")[:1]
        user.username = profile_json.get("response").get("nickname")
        token, created = Token.objects.get_or_create(user = user)
        user.save()
        token_value = token.key
        accept_json['token'] = token_value

        return JsonResponse(accept_json)

class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = NAVER_REDIRECT_URI
    client_class = OAuth2Client