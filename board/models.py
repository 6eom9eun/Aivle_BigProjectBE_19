from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Profile
import os

"""
    post_id : 글 번호
    user : 작성자
    title: 제목
    content: 내용
    created_at: 작성일
    published_at: 배포일(수정일)
"""
class Post(models.Model):
    post_id = models.AutoField(primary_key=True) # 기본키
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True) # 외래키
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)  # 사진 첨부
        
    def publish(self):
        self.published_at = timezone.now()
        self.save()

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
class Comment(models.Model): # 해당 글의 댓글 관리
    """
        comment_id : 댓글 번호
        user : 사용자
        reply: Reply -> Post 연결관계
        comment: 댓글내용
        created_at: 작성일
    """
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, db_index=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    comment_id = models.AutoField(primary_key=True) # 기본키
    reply = models.ForeignKey(Post, related_name='comments', null=False, blank=False, on_delete=models.CASCADE, db_index=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    
    def __str__(self):
        return self.comment
    
    # Foreign Key로는 user(댓글 쓴 사람)와 reply(게시글) 모델을 연결