from django.urls import path
from .views import *

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz-list'),
    path('quiz/', RandomQuizView.as_view(), name='quiz-random'),
    path('quiz/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
]