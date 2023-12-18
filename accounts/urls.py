from django.urls import path
from .views import signupView, CustomLoginView, profileView

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profileView, name='profile'),
]