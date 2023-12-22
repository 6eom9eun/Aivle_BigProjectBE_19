from rest_framework import permissions

# 권한 수정
class CustomReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 데이터에 영향을 미치지 않는 메소드 (GET 등)은 통과
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT/PATCH 등의 경우에는 요청으로 들어온 유저와 객체의 유저를 비교해 같으면 통과
        return obj.user == request.user