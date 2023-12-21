from django.urls import path
from .views import RandomQuizView

urlpatterns = [
    path('quiz/', RandomQuizView.as_view()),
]