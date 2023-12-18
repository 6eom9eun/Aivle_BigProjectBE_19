from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm): # 회원가입 폼
    class Meta:
        model = CustomUser
        fields = ('user_id', 'email', 'password1', 'password2', 'first_name', 'last_name')

class CustomLoginForm(AuthenticationForm): # 로그인 폼
    class Meta:
        model = CustomUser
        fields = ('username', 'password')