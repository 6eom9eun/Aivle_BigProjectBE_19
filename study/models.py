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
    is_correct = models.BooleanField(default=False)
    solved_date = models.DateTimeField(auto_now_add=True)

class Audio(models.Model):
    audio_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    audio = models.FileField(upload_to='audio/')