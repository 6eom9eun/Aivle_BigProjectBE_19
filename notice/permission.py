from rest_framework import permissions

class AdminPermission(permissions.BasePermission):
    message = '관리자만 접근할 수 있습니다.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (request.user and request.user.is_authenticated and request.user.is_staff)