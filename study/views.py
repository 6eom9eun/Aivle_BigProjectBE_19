from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Word, Quiz
from .gpt import *
from .text_speech import *
from .spell_correct import *
from .serializers import *
from django.http import JsonResponse
import random

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

            # 정답 추출
            idx = None
            for index, answer in enumerate(response['questions'][0]['answers']):
                if answer['correct']:
                    idx = index
                    break

            # 사용자에게 응답 반환 및 정답 저장
            quiz_instance = Quiz(
                user=request.user,
                word=random_word_entry,
                quiz=response,
                answer=idx
            )
            quiz_instance.save()
            
            response_with_word_meaning = {
                'word': word,
                'meaning': meaning,
                'question_response': response
            }

            return JsonResponse(response_with_word_meaning, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "데이터베이스에서 단어를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class QuizListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#######
class SpellCorrect(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        quizzes = Quiz.objects.filter(user=user, solved_date__isnull=False).order_by('-quiz_id')[:5]

        quiz_data = [{quiz} for quiz in quizzes]

        return Response(quiz_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        sentence = request.data.get('sentence', '')
        
        if not sentence:
            return Response({'error': '요청 데이터에 문장이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.request.user
        quizzes = Quiz.objects.filter(user=user, solved_date__isnull=False).order_by('-quiz_id')[:5]

        words = [quiz.word.word_text for quiz in quizzes]

        result = is_correct(sentence, words)
        return Response(result, status=status.HTTP_200_OK)
#########


class TextToSpeechView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        sentence = request.data.get('sentence')# JSON {"sentence": "안녕하세요. 반갑습니다."}
        Text_To_Speech(sentence)
        return Response({'message': 'Text-to-Speech 변환 성공'}, status=status.HTTP_200_OK)

class SpeechToTextView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        file_path = request.data.get('file_path') # '{"file_path": "/media/stt/file.wav"}' 실제 오디오 파일 경로 변경
        transcript = Speech_To_Text(file_path)
        return Response({'transcript': transcript}, status=status.HTTP_200_OK)
    
