from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from .forms import UserCreationForm, CustomLoginForm

from django.contrib.auth.models import User

def signupView(request): # 회원가입 뷰
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            if User.objects.filter(username=username).exists(): # 아이디 존재 확인
                messages.error(request, '이미 존재하는 사용자 ID 입니다.')
            else:
                user = form.save()

                authenticated_user = authenticate(
                    request,
                    username=username,
                    password=form.cleaned_data['password1']
                )

                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, '가입 및 로그인 성공')
                    return redirect('profile')
                else:
                    messages.error(request, '로그인에 실패했습니다.')
        else:
            messages.error(request, '가입에 실패하였습니다. 올바른 정보를 입력해주세요.')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView): # 로그인 뷰
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패했습니다. 올바른 정보를 입력해주세요.')
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '로그인 성공')
        return response
    
def profileView(request):  # 프로필 뷰
    return render(request, 'accounts/profile.html', {'user': request.user})

def logoutView(request): # 로그아웃 뷰
    logout(request)
    messages.success(request, '로그아웃 되었습니다.')
    return redirect('login')
