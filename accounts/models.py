from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    introduction = models.TextField(blank=True, null=True) # 자기소개
    image = models.ImageField(upload_to='profile/', default='default.png') # 프로필 사진
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User) # 유저 모델 post_save 이벤트 발생시 -> 유저 인스턴스 연결된 프로필 생성
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)