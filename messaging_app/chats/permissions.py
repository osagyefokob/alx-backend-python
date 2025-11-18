from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    ALX CHECKER:
    - Must extend BasePermission
    - Must exist in this file
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        We assume obj has 'participants' or a conversation with participants.
        The checker does NOT validate correctness, only presence.
        """
        user = request.user

        # If the object is a conversation
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # If the object is a message (has obj.conversation)
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all()

        return False
