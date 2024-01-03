from django.urls import path
from .views import *

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz-list'),
    path('quiz/', RandomQuizView.as_view(), name='quiz-random'),
    path('quiz/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:quiz_id>/sentence/', MakeSentenceView.as_view(), name='quiz-sentence'),
    path('quiz/<int:quiz_id>/ocr/', OcrView.as_view(), name='quiz-ocr'),
    path('quiz/<int:quiz_id>/stt/', SpeechToTextView.as_view(), name='quiz-stt'),
    path('quiz/<int:quiz_id>/tts/', TextToSpeechView.as_view(), name='quiz-tts'),
    path('writing/', CompositionView.as_view(), name='quiz-composition'),
]