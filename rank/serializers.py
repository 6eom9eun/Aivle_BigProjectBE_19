from rest_framework import serializers
from .models import Ranking

class RankingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Ranking
        fields = ['user_id', 'username', 'user_level', 'answers', 'created_dt']