from django.db import models

from rest_framework import serializers
from .models import ChatPrompt

class ChatPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatPrompt
        fields = ['word', 'meaning']