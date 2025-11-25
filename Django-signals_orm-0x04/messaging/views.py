# ALX Task 4: unread inbox view

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def unread_inbox(request):
    """
    Displays unread messages for the logged-in user.
    Uses custom manager + .only() optimization.
    """
    unread_msgs = Message.unread.unread_for_user(request.user)

    # Example display (template not required for ALX)
    return render(request, "messaging/unread_inbox.html", {
        "messages": unread_msgs
    })
