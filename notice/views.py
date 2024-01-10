from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.authentication import TokenAuthentication
from .permission import AdminPermission

class NoticeListView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
