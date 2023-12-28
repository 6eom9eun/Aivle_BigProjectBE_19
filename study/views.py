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

class CompositionView(APIView): # 작문뷰 만드는 중
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자의 최근 5개 퀴즈 가져오기
        last_quizzes = Quiz.objects.filter(user=request.user).order_by('-quiz_id')[:5]

        if len(last_quizzes) < 5:
            return JsonResponse({"error": "아직 충분한 수의 퀴즈가 완료되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 최근 5개 퀴즈에서 2개의 무작위 단어 가져오기
        selected_words = [quiz.word.word for quiz in last_quizzes]

        # 중복 제거
        selected_words = list(set(selected_words))

        if len(selected_words) < 2:
            return JsonResponse({"error": "충분한 고유한 단어가 발견되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자에게 2개의 단어 선택하도록 요청
        # 이 부분을 사용자가 직접 선택하도록 변경
        # 예를 들어, 선택된 단어를 URL 쿼리 매개변수로 전달받을 수 있습니다.
        # /study/composition/?selected_words=단어1,단어2
        selected_words_by_user = request.GET.getlist('selected_words')

        if len(selected_words_by_user) != 2 or not all(word in selected_words for word in selected_words_by_user):
            return JsonResponse({"error": "유효하지 않은 단어 선택입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 선택된 단어를 사용하여 작문 생성
        composition_words = selected_words_by_user  # 사용자가 선택한 단어를 사용

        # korean_pos_tagging 및 is_correct 함수를 사용하여 작문 로직을 구현하세요
        composition_text = " ".join(composition_words)  # 예: 선택된 단어를 공백으로 연결

        # 작문이 올바른지 확인
        composition_result = is_correct(composition_text, selected_words)

        response_data = {
            'selected_words': selected_words,
            'selected_words_by_user': selected_words_by_user,
            'composition_text': composition_text,
            'composition_result': composition_result
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)


class QuizListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user)
        serializer = QuizListSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'quiz_id'
    
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
    
