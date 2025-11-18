from rest_framework import viewsets
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipantOfConversation]


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipantOfConversation]
