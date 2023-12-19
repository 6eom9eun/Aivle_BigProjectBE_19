from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
"""
    post_id : 글 번호
    user : 작성자
    title: 제목
    content: 내용
    created_at: 작성일
    published_at: 배포일(수정일)
"""
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()
        
class Comment(models.Model): # 해당 글의 댓글 관리
    """
        reply: Reply -> Post 연결관계
        comment: 댓글내용
        rep_date: 작성일
    """
    reply = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rep_date = models.DateTimeField()

    def __str__(self):
        return self.comment