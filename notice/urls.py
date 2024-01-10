from django.urls import path
from .views import NoticeListView, NoticeDetailView

urlpatterns = [
    path('', NoticeListView.as_view(), name='notice-list-create'),
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
]