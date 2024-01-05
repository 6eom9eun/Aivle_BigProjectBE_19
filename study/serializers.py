from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *


# 퀴즈 시리얼라이저
class QuizSerializer(serializers.ModelSerializer):
    word = serializers.CharField(source='word.word', read_only=True)
    
    class Meta:
        model = Quiz
        fields = '__all__'
        
    def update(self, instance, validated_data):
        new_chat_log = validated_data.get('chat_log', '')
        
        # if instance.chat_log:
        #     instance.chat_log += f"\n{new_chat_log}"
        # else:
        #     instance.chat_log = new_chat_log
        instance.chat_log = new_chat_log
            
        instance.solved_date = validated_data.get('solved_date', instance.solved_date)

        instance.save()
        return instance

# 퀴즈 리스트 시리얼라이저    
class QuizListSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    word = serializers.CharField(source='word.word', read_only=True)
    meaning = serializers.CharField(source='word.meaning', read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['quiz_id', 'word', 'meaning', 'solved_date', 'username']