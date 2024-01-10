from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Ranking(models.Model):
    lv_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ranking') 
    user_level = models.IntegerField(default=1) #단어장 레벨
    answers = models.IntegerField(default=0)  #푼 문제수
    created_dt=models.DateTimeField(null=True, blank = True, auto_now_add=True)      #수정날짜 표시(등수 같을 경우 순위 판단)
    
    def publish(self):
        self.created_dt = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
            if self.pk is not None:
                original_ranking = Ranking.objects.get(pk=self.pk)
                if original_ranking.answers != self.answers:
                    self.created_dt = timezone.now()
            super(Ranking, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - Level {self.user_level} {self.created_dt}"
    
@receiver(post_save, sender=User)
def create_user_ranking(sender, instance, created, **kwargs):
    if created:
        Ranking.objects.get_or_create(user=instance)

post_save.connect(create_user_ranking, sender=User)