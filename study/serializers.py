from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class QuizSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    word = serializers.CharField(source='word.word', read_only=True)
    meaning = serializers.CharField(source='word.meaning', read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['quiz_id', 'word', 'meaning', 'solved_date', 'username']