from rest_framework import permissions

## 게시글 ==> 조회는 누구나 가능 / 작성은 로그인한 유저만 / 수정, 삭제는 작성자만
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):        
        # 읽기 권한 요청이 들어오면 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 요청자(request.user)가 객체(Board)의 user와 동일한지 확인
        return obj.user == request.user

class CustomReadOnly(permissions.BasePermission):
    ## 게시글 ==> 조회는 누구나 가능 / 작성은 로그인한 유저만 / 수정은 작성자만
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        return False
    
    # 각 객체별 권한
    def has_object_permission(self, request, view, obj):
        # 안전한 메서드(GET, HEAD, OPTIONS)로 요청이 들어오면 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # PUT/PATCH 등의 경우에는 요청으로 들어온 유저와 객체의 유저를 비교해 같으면 통과
        # 요청자(request.user)가 객체(Post)의 user와 동일한지 확인
        return obj.user == request.user