from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer, NoticeListSerializer, NoticeCreateSerializer
from rest_framework.authentication import TokenAuthentication
from .permission import AdminPermission
from .models import Notice

class NoticeListView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    queryset = Notice.objects.order_by('-id')
    
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return NoticeCreateSerializer
        return NoticeListSerializer
    
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer