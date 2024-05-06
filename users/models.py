from django.contrib.auth.models import User
from django.db import models
from random import randint


class OneTimeCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
