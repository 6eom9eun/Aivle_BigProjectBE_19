from django.urls import path
from .views import *
urlpatterns = [
    path('', UserDetailView.as_view()),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('update/', UserUpdateView.as_view()),
    ]