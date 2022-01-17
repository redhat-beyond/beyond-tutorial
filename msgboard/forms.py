from django import forms
from .models import Message, UserMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('author', 'text')


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ('text',)
