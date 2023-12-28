from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Word, Quiz
from .ai.gpt import *
from .ai.text_speech import *
from .ai.spell_correct import *
from .serializers import *
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q # OR 조건, 부정, 그리고 조합과 관련된 복잡한 쿼리
from django.urls import reverse
from django.shortcuts import redirect

# 랜덤 퀴즈 생성 뷰
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
                quiz=json.dumps(response),
                answer=idx
            )
            quiz_instance.save()

            # 새로 생성된 퀴즈의 quiz_id를 사용하여 상세 페이지로 리다이렉션
            return redirect(reverse('quiz-detail', kwargs={'quiz_id': quiz_instance.quiz_id}))
        else:
            return JsonResponse({"error": "데이터베이스에서 단어를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

# 퀴즈 리스트 뷰       
class QuizListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 퀴즈 디테일 뷰
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    lookup_field = 'quiz_id'

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

# 작문 뷰
class CompositionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자의 최근 5개 맞춘 퀴즈 가져오기
        resolved_quizzes = Quiz.objects.filter(
            Q(user=request.user) & ~Q(solved_date=None)
        ).order_by('-quiz_id')[:5]

        if len(resolved_quizzes) < 5:
            return JsonResponse({"error": "아직 충분한 수의 퀴즈가 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 퀴즈에서 5개의 단어 가져오기
        quiz_words = [quiz.word for quiz in resolved_quizzes]

        # 사용자에게 2개의 단어 선택하도록 요청
        selected_word_ids_by_user = request.GET.getlist('selected_words')

        if len(selected_word_ids_by_user) != 2:
            return JsonResponse({"error": "단어를 2개 선택하세요."}, status=status.HTTP_400_BAD_REQUEST)

        selected_words = Word.objects.filter(id__in=selected_word_ids_by_user)

        if len(selected_words) != 2:
            return JsonResponse({"error": "올바른 단어 ID를 선택하세요."}, status=status.HTTP_400_BAD_REQUEST)
        selected_words_info = [{'word': word.word, 'meaning': word.meaning} for word in selected_words]

        # 선택된 단어를 사용하여 작문
        composition_words = selected_words_info
        composition_text = request.GET.get('composition_text', '')

        # 작문이 올바른지 확인, spell_correct.py 모델 사용
        composition_result = is_correct(composition_text, composition_words)

        response_data = {
            'composition_text': composition_text,
            'composition_words': composition_words,
            'composition_result': composition_result
        }
        
        return JsonResponse(response_data, status=status.HTTP_200_OK)

# TTS 뷰  
class TextToSpeechView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        sentence = request.data.get('sentence')# JSON {"sentence": "안녕하세요. 반갑습니다."}
        Text_To_Speech(sentence)
        return Response({'message': 'Text-to-Speech 변환 성공'}, status=status.HTTP_200_OK)

# STT 뷰
class SpeechToTextView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        file_path = request.data.get('file_path') # '{"file_path": "/media/stt/file.wav"}' 실제 오디오 파일 경로 변경
        transcript = Speech_To_Text(file_path)
        return Response({'transcript': transcript}, status=status.HTTP_200_OK)
    
