from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from .forms import SignupForm, CustomLoginForm

def signupView(request): # 회원가입 뷰
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signup')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView): # 로그인 뷰
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '로그인 성공')

        return response
    
def profileView(request): # 프로필 뷰
    return render(request, 'accounts/profile.html', {'user': request.user})