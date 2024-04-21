from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    date_joined = models.DateTimeField(auto_now_add=True)
    