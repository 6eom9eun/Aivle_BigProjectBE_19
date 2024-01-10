from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer, NoticeListSerializer, NoticeCreateSerializer
from .permission import AdminPermission
from .models import Notice

class NoticeListView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [AdminPermission]
    queryset = Notice.objects.order_by('-id')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NoticeCreateSerializer
        return NoticeListSerializer
    
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = [AdminPermission]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer