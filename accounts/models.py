from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rank.models import Ranking

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    introduction = models.TextField(default="안녕하세요", blank=True, null=True)  # 자기소개
    image = models.ImageField(upload_to='profile/', default='default_profile.png')  # 프로필 사진

    def __str__(self):
        return self.user.username
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance) # 모델에서, 인스턴스와 일치하는 거 찾기, 아니면 생성