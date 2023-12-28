from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Word, Quiz
from .gpt import *
from .text_speech import *
from .spell_correct import *
from .serializers import *
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q # OR 조건, 부정, 그리고 조합과 관련된 복잡한 쿼리

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
        
class QuizListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    lookup_field = 'quiz_id'

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)
    
class CompositionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자의 최근 5개 맞춘 퀴즈 가져오기
        resolved_quizzes = Quiz.objects.filter(
            Q(user=request.user) & ~Q(solved_date=None) # 사용자 and solved_date가 none이 아닌 것 ORDER BY DESC
        ).order_by('-quiz_id')[:5]

        if len(resolved_quizzes) < 5:
            return JsonResponse({"error": "아직 충분한 수의 퀴즈가 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자에게 2개의 단어 선택하도록 요청
        selected_words_by_user = request.GET.getlist('selected_words')

        if len(selected_words_by_user) != 2:
            return JsonResponse({"error": "단어를 2개 선택하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 선택된 단어를 사용하여 작문
        composition_words = selected_words_by_user
        composition_text = " ".join(composition_words)

        # 작문이 올바른지 확인
        composition_result = is_correct(composition_text)

        response_data = {
            'selected_words_by_user': selected_words_by_user,
            'composition_text': composition_text,
            'composition_result': composition_result
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
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
    
