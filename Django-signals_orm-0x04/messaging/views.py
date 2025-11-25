# ALX Task 2: Delete user account and trigger cleanup via post_delete signal

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def delete_user(request):
    """
    Deletes the currently logged-in user's account.
    This will trigger the post_delete signal to clean up:
    - Messages sent/received by this user
    - Notifications for this user
    - MessageHistory records tied to messages of this user
    """

    user = request.user
    user.delete()  # This will automatically trigger post_delete signal

    return redirect("/")  # Send user to homepage after deletion
