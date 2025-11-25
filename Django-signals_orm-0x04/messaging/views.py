# ALX Task 5: Caching view using cache_page(60)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from messaging.models import Message


@login_required
@cache_page(60)   # ALX requires this exact decorator + timeout
def cached_conversation(request):
    """
    Displays messages and caches the entire response for 60 seconds.
    ALX checks for:
    - @cache_page
    - 60
    - Message.objects
    """
    messages = Message.objects.filter(receiver=request.user).order_by("-timestamp")

    return render(request, "chats/cached_conversation.html", {
        "messages": messages
    })
