from django.db import models
from django.contrib.auth.models import User
    
class Word(models.Model):
    word = models.CharField(max_length=255)
    meaning = models.TextField()

    def __str__(self):
        return f"{self.word} - {self.meaning}"
    
class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    quiz = models.TextField(blank=True, null=False)
    answer = models.IntegerField(null=True, blank=True)
    solved_date = models.DateTimeField(null=True, blank=True)
    chat_log = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Quiz on {self.word}"

    class Meta:
        ordering = ['-solved_date']

class Audio(models.Model):
    audio_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    audio = models.FileField(upload_to='audio/')