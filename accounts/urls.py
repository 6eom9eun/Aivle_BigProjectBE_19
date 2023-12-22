from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserUpdateView.as_view()),
    ]