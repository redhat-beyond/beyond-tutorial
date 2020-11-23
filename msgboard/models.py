from django.db import models
from django.utils import timezone

from accounts.models import Account


class Message(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class UserMessagesManager(models.Manager):
    def main_feed(self):
        return self.order_by('-date').select_related()


class UserMessage(models.Model):
    author = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    messages = UserMessagesManager()
