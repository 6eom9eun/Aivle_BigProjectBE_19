from django.db import models
from django.contrib.auth.models import User

class Ranking(models.Model):
    lv_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ranking') 
    user_level = models.IntegerField() #단어장 레벨
    answers = models.IntegerField(default=0)  #푼 문제수
    created_dt=models.DateTimeField(auto_now_add=True)       #수정날짜 표시(등수 같을 경우 순위 판단)

    def __str__(self):
        return f"{self.user.username} - Level {self.user_level}"