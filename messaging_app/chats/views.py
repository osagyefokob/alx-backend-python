# messaging_app/chats/views.py

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import StandardResultsSetPagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Only return conversations the requesting user participates in
        user = self.request.user
        return Conversation.objects.filter(participants=user).distinct()


class MessageViewSet(viewsets.ModelViewSet):
    """
    Messages are paginated 20 per page and support filtering by:
    - participant (user id)
    - created_after / created_before (ISO datetimes)
    """
    queryset = Message.objects.select_related("conversation", "sender").all().order_by("-created_at")
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    ordering_fields = ["created_at"]
    search_fields = ["content"]

    def get_queryset(self):
        """
        If the view is nested under a conversation (conversation_pk in kwargs),
        limit to that conversation. Otherwise show messages for conversations
        the user participates in.
        """
        user = self.request.user
        conv_pk = self.kwargs.get("conversation_pk")
        qs = self.queryset

        if conv_pk:
            qs = qs.filter(conversation__pk=conv_pk)
        else:
            qs = qs.filter(conversation__participants=user)

        return qs.distinct()

    def perform_create(self, serializer):
        # Ensure sender is the logged-in user
        serializer.save(sender=self.request.user)
