from django.db import models
from django.contrib.auth.models import User

class Ranking(models.Model):
    lv_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ranking')
    user_level = models.IntegerField()
    answers = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Level {self.user_level}"