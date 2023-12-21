from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    ## 게시글 ==> 조회는 누구나 가능 / 작성은 로그인한 유저만 / 수정은 작성자만
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        return False
    
    # 각 객체별 권한
    # SAFE_METHOD(GET, HEAD, OPTIONS)로 요청이 들어온 경우에는 method를 허용을 해주고,
    # 그 외(PUT, PATCH, DELETE)에는 게시글의 user와 로그인된 user가 동일한 경우에만 권한을 허용
    def has_object_permission(self, request, view, obj):
        # 데이터에 영향을 미치지 않는 메소드 (GET 등)은 통과
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT/PATCH 등의 경우에는 요청으로 들어온 유저와 객체의 유저를 비교해 같으면 통과
        return obj.author == request.user