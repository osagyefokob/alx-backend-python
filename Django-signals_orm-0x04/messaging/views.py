from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message

@cache_page(60)  # 60 seconds cache timeout
@login_required
def conversation_list(request):
    """
    View placeholder that would list messages for the logged in user.
    Caching is applied per the milestone requirements.
    """
    user = request.user
    messages = Message.unread_for_user(user) if hasattr(Message, "unread_for_user") else Message.objects.filter(receiver=user)
    return render(request, "messaging/conversation_list.html", {"messages": messages})
