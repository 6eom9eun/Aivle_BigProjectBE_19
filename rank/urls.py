from django.urls import path
from .views import RankingListView

urlpatterns = [
    path('', RankingListView.as_view()),
]