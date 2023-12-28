from django.urls import path
from .views import *

urlpatterns = [
    path('', QuizListView.as_view()),
    path('quiz/', RandomQuizView.as_view()),
    path('quiz/<int:quiz_id>/', QuizDetailView.as_view()),
]