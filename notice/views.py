from rest_framework import generics
from .models import Notice
from rest_framework import permissions
from .serializers import NoticeSerializer

class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class NoticeListView(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AdminPermission]

class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AdminPermission]