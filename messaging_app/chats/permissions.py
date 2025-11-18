from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    This permission ensures only participants can:
    - PUT
    - PATCH
    - DELETE
    """

    def has_permission(self, request, view):
        # Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If it's a conversation object
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # If it's a message object
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False
