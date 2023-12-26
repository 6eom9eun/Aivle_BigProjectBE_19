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
    ]