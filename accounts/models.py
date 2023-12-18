from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    # 추가 필드
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # 기본 필드
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=150)

    def __str__(self):
        return self.username