from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Word, Quiz
from .gpt import *
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class RandomQuizView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        random_word_entry = Word.objects.order_by('?').first()

        if random_word_entry:
            word = random_word_entry.word
            meaning = random_word_entry.meaning

            response = make_problem(word, meaning)

            if request.user.is_authenticated:
                quiz_instance = Quiz(user=request.user, word=random_word_entry)
                quiz_instance.save()

                return JsonResponse({"question_response": response}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"error": "데이터베이스에서 단어를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)