from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Word
from .gpt import *
from django.http import JsonResponse

class RandomQuizView(APIView):
    def get(self, request):
        # 데이터베이스에서 무작위 레코드 단어와 뜻을 가져옴
        random_word_entry = Word.objects.order_by('?').first()
        print(random_word_entry.word)
        if random_word_entry:
            # 랜덤 항목에서 단어와 뜻 추출
            word = random_word_entry.word
            meaning = random_word_entry.meaning

            # 질문 생성
            response = make_sentence(word, meaning)

            # 사용자에게 응답 반환
            return JsonResponse({"question_response": response}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "데이터베이스에서 단어를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
