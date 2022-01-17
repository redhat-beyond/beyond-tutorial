from django.db import models
from django.utils import timezone

from accounts.models import Account


class Message(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class UserMessage(models.Model):
    author = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
