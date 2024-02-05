from rest_framework import generics

from .models import Ranking
from .serializers import RankingSerializer

# Ranking 목록 조회 뷰
class RankingListView(generics.ListAPIView):
    queryset = Ranking.objects.select_related('user').order_by('-user_level', 'created_dt')  # 사용자 레벨 내림차순, 먼저 맞춘 사람이 등수 위 
    serializer_class = RankingSerializer
    
