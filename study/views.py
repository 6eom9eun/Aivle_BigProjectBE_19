from django.http import JsonResponse, FileResponse
from django.db.models import Q # OR 조건, 부정, 그리고 조합과 관련된 복잡한 쿼리
from django.urls import reverse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

import json
from paddleocr import PaddleOCR

from .models import Word, Quiz
from .new_gpt import *
from .text_speech import *
from .spell_correct import *
from .serializers import *

# 랜덤 퀴즈 생성 뷰
class RandomQuizView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 데이터베이스에서 무작위 레코드 단어와 뜻을 가져옴
        try:
            random_word_entry = Word.objects.order_by('?').first()

            if random_word_entry:
                # 랜덤 항목에서 단어와 뜻 추출
                word = random_word_entry.word
                meaning = random_word_entry.meaning

                # 질문 생성
                response = make_problem(word, meaning)

                # # 정답 추출
                # idx = None
                # for index, answer in enumerate(response['questions'][0]['answers']):
                #     if answer['correct']:
                #         idx = index
                #         break

                # 사용자에게 응답 반환 및 정답 저장
                quiz_instance = Quiz(
                    user=request.user,
                    word=random_word_entry,
                    quiz=json.dumps(response),
                    # answer=idx
                )
                quiz_instance.save()
                # 새로 생성된 퀴즈의 quiz_id를 사용하여 상세 페이지로 리다이렉션
                return redirect(reverse('quiz-detail', kwargs={'quiz_id': quiz_instance.quiz_id}))
            else:
                raise ValidationError("데이터베이스에서 단어를 찾을 수 없습니다.")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# gpt가 작문 뷰
class MakeSentenceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        try:
            word = request.data.get('word', '')
            meaning = request.data.get('meaning', '')

            response = make_sentence(word, meaning)

            return JsonResponse(response, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 퀴즈 리스트 뷰       
class QuizListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            quizzes = Quiz.objects.filter(user=request.user)
            serializer = QuizListSerializer(quizzes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 퀴즈 디테일 뷰
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer
    lookup_field = 'quiz_id'

    def get_queryset(self):
        try:
            return Quiz.objects.filter(user=self.request.user)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 직접 작문하기 뷰
class CompositionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자의 최근 5개 맞춘 퀴즈 가져오기
        try:
            resolved_quizzes = Quiz.objects.filter(
                Q(user=request.user) & ~Q(solved_date=None)
            ).order_by('-quiz_id')[:5]

            if len(resolved_quizzes) < 5:
                return JsonResponse({"error": "아직 충분한 수의 퀴즈가 완료되지 않았습니다."}, status=status.HTTP_201_CREATED)

            # 최근 맞춘 5개의 퀴즈에서 5개의 단어 가져오기
            quiz_words = [{'id': quiz.word.id, 'word': quiz.word.word, 'meaning': quiz.word.meaning} for quiz in resolved_quizzes]

            # 사용자에게 5개의 단어 보여주기
            return JsonResponse({"quiz_words": quiz_words}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        # 사용자는 단어 2개 고르기
        try:
            selected_word_by_user = json.loads(request.data.get('selected_words', []))

            if len(selected_word_by_user) < 2:
                return JsonResponse({"error": "단어를 2개 이상 선택해야 합니다. 재접속 후 다시 진행해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

            selected_words = Word.objects.filter(id__in=selected_word_by_user)

            if len(selected_words) < 2:
                return JsonResponse({"error": "올바른 단어 ID를 선택해야 합니다. 재접속 후 다시 진행해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

            selected_words_info = [{'word': word.word, 'meaning': word.meaning} for word in selected_words]

            # 선택된 단어를 사용하여 작문
            composition_words = [word['word'] for word in selected_words_info]
            print(composition_words)
            composition_text = request.data.get('composition_text', '')
            print(composition_text)
            # 작문이 올바른지 확인, spell_correct.py 모델 사용
            composition_result = is_correct(composition_text, composition_words)

            response_data = {
                'composition_text': composition_text,
                'composition_words': composition_words,
                'composition_result': composition_result
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# OCR API 뷰
class OcrView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            image_data = request.data.get('image')

            if image_data:
                # 이미지를 파일로 저장하지 않고 바이트 데이터를 사용하여 OCR 수행
                ocr = PaddleOCR(lang="korean")
                result = ocr.ocr(image_data.read(), cls=False)
                text_results = []

                for line in result:
                    paragraph = ""
                    for word_info in line:
                        try:
                            if isinstance(word_info, list) and len(word_info) == 4 and all(isinstance(point, list) and len(point) == 2 for point in word_info):
                                pass
                            elif isinstance(word_info, tuple) and len(word_info) == 2 and isinstance(word_info[0], str) and isinstance(word_info[1], (int, float)):
                                word_text, _ = word_info
                                paragraph += word_text + " "
                            else:
                                print(f"예기치 않은 구조 in word_info: {word_info}")
                        except (TypeError, ValueError) as e:
                            print(f"처리 중 에러 word_info: {e}")

                    if paragraph.strip():
                        text_results.append(paragraph.strip())
                    
                    # 문장 만들기
                    sentence=''
                    for temp in text_results:
                        sentence+=(' '+temp)        # 앞에 공백을 처리해서 문장으로 변환
                    
                    # 정답 텍스트 불러오기
                    text = request.data.get('text', '')
                    print(text)
                    correct=response_is_correct(text, sentence)
                
                return JsonResponse({'text_results': text_results, 'answer':correct}, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError("이미지가 없습니다.")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# TTS API 뷰
class TextToSpeechView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # 클라이언트에서 POST 요청으로 텍스트를 받아옴
            text = request.data.get('text', '')

            # 텍스트를 음성으로 변환
            tts = gTTS(text=text, lang="ko", slow=False)
            
            # 임시 파일로 저장 = 데이터가 쌓이지 않음
            mp3_file_path = "study/tmp/speech.mp3"
            tts.save(mp3_file_path)

            # 브라우저로 음성 파일을 전송
            response = FileResponse(open(mp3_file_path, 'rb'))
            response['Content-Type'] = 'audio/mp3'
            response['Content-Disposition'] = 'inline; filename=speech.mp3'
            
            return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# STT API 뷰
class SpeechToTextView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            audio_file = request.FILES.get('audio', None)
            if not audio_file:
                return Response({"error": "오디오파일 받지않았음."}, status=400)

            # 오디오 파일을 임시로 저장 = 데이터가 쌓이지 않음
            audio_file_path = "study/tmp/audio.wav"
            with open(audio_file_path, 'wb') as file:
                for chunk in audio_file.chunks():
                    file.write(chunk)
        
            # 음성을 텍스트로 변환
            transcript = Speech_To_Text(audio_file_path)
            
            # 정답 텍스트 불러오기
            text = request.data.get('text', '')
            print(text)
            correct=response_is_correct(text, transcript)
            
            # return Response({"text": transcript.get('text', '')}, status=status.HTTP_200_OK)
            # return Response({"text": transcript}, status=status.HTTP_200_OK)
            return Response({"text": transcript, "answer":correct}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)