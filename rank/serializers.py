from rest_framework import serializers
from .models import Ranking

# 랭킹 시리얼라이저
class RankingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Ranking
        fields = ['user_id', 'username', 'user_level', 'answers', 'created_dt']