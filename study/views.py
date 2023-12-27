from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Word, Quiz
from .gpt import *
from .text_speech import *
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class RandomQuizView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 데이터베이스에서 무작위 레코드 단어와 뜻을 가져옴
        random_word_entry = Word.objects.order_by('?').first()

        if random_word_entry:
            # 랜덤 항목에서 단어와 뜻 추출
            word = random_word_entry.word
            meaning = random_word_entry.meaning

            # 질문 생성
            response = make_problem(word, meaning)

            # 사용자에게 응답 반환
            quiz_instance = Quiz(user=request.user, word=random_word_entry, quiz=response)
            quiz_instance.save()

            return JsonResponse({"question_response": response}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "데이터베이스에서 단어를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        

class TextToSpeechView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        sentence = request.data.get('sentence')
        Text_To_Speech(sentence)
        return Response({'message': 'Text-to-Speech 변환 선공'}, status=status.HTTP_200_OK)

class SpeechToTextView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        file_path = request.data.get('file_path')
        transcript = Speech_To_Text(file_path)
        return Response({'transcript': transcript}, status=status.HTTP_200_OK)