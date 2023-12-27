from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Word, Quiz
from .gpt import *
from .text_speech import *
from .spell_correct import *
from .serializers import *
from django.http import JsonResponse
from django.utils import timezone

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
            
            response = {
                'word': word,
                'meaning': meaning,
                'question_response': response
            }

            return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "데이터베이스에서 단어를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
    # 사용자 문제 풀기
    # def post(self, request):
    #     # 요청에서 데이터 가져오기
    #     user_answer = request.data.get('user_answer')  # 사용자의 답변이 요청 데이터
    #     # 요청 데이터 유효성 검사
    #     if user_answer is None:
    #         return JsonResponse({"error": "user_answer는 요청 데이터에 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    #     # 사용자에 대한 퀴즈 인스턴스 가져오기
    #     quiz_instance = Quiz.objects.filter(user=request.user, solved_date__isnull=True).first()

    #     if quiz_instance:
    #         # 사용자의 답변이 정답과 일치하는지 확인
    #         if quiz_instance.answer == int(user_answer):
    #             # 정답이 맞으면 solved_date를 현재 타임스탬프로 갱신
    #             quiz_instance.solved_date = timezone.now()
    #             quiz_instance.save()

    #             return JsonResponse({"message": "정답입니다! 풀이 날짜가 갱신되었습니다."}, status=status.HTTP_200_OK)
    #         else:
    #             return JsonResponse({"message": "틀린 답변입니다. 다시 시도해보세요!"}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return JsonResponse({"error": "사용자에 대한 활성화된 퀴즈가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        

class QuizListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
