from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Message

@cache_page(60)
def conversation_view(request):
    user = request.user
    messages = Message.unread.unread_for_user(user)
    return render(request, 'conversation.html', {'messages': messages})
