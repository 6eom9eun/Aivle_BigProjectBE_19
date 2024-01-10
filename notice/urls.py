from django.urls import path
from .views import NoticeListView, NoticeDetailView

app_name = 'notice'
urlpatterns = [
    path('', NoticeListView.as_view(), name='notice-list'),
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
]