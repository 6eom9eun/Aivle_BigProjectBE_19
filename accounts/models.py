from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    # MBTI = [
    # ('mbti_istj', 'ISTJ'),
    # ('mbti_istp', 'ISTP'),
    # ('mbti_isfj', 'ISFJ'),
    # ('mbti_isfp', 'ISFP'),
    # ('mbti_intj', 'INTJ'),
    # ('mbti_intp', 'INTP'),
    # ('mbti_infj', 'INFJ'),
    # ('mbti_infp', 'INFP'),
    # ('mbti_estj', 'ESTJ'),
    # ('mbti_estp', 'ESTP'),
    # ('mbti_esfj', 'ESFJ'),
    # ('mbti_esfp', 'ESFP'),
    # ('mbti_entj', 'ENTJ'),
    # ('mbti_entp', 'ENTP'),
    # ('mbti_enfj', 'ENFJ'),
    # ('mbti_enfp', 'ENFP'),
    # ('mbti_none', '선택안함'),
    # ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    introduction = models.TextField(default="안녕하세요", blank=True, null=True)  # 자기소개
    image = models.ImageField(upload_to='profile/', default='default_profile.png')  # 프로필 사진
    # mbti = models.CharField(max_length=30, choices=MBTI, default="mbti_none")

    def __str__(self):
        return self.user.username
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance) # 모델에서, 인스턴스와 일치하는 거 찾기, 아니면 생성