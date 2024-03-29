from django.shortcuts import render, redirect
from .models import UserMessage
from .forms import UserMessageForm


def board(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UserMessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user.account
                message.save()
                return redirect('board')
        else:
            form = UserMessageForm()
    else:
        if request.method == "POST":
            return redirect('board')
        form = None
    messages = UserMessage.messages.main_feed()
    return render(request, 'msgboard/board.html', {
        'messages': messages,
        'form': form,
    })
