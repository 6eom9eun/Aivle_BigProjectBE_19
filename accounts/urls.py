from django.urls import path
from .views import * 

urlpatterns = [
    path('user/', UserDetailView.as_view()),
    path('user/update/', UserUpdateView.as_view()),
    path('profile/', ProfileDetailView.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),
    path('profile/<int:user_id>/', OtherUserProfileView.as_view()),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    
    path('kakao/login/', kakao_login, name='kakao_login'),
    path('kakao/callback/', kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
    
    path('naver/login/', naver_login, name='naver_login'),
    path('naver/callback/', naver_callback, name='naver_callback'),
    path('naver/login/finish/', NaverLogin.as_view(), name='naver_login_todjango'),

 ]