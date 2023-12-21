from rest_framework import generics
from .models import Ranking
from .serializers import RankingSerializer

class RankingListView(generics.ListAPIView):
    queryset = Ranking.objects.order_by('-answers', 'user_level') # 푼 문제 수로 내림차순, 그 다음 사용자 레벨 오름차순
    serializer_class = RankingSerializer
    