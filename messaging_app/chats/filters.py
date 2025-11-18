# messaging_app/chats/filters.py

import django_filters
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    """
    Filters:
    - participant: user id of a conversation participant (messages in conversations that include this user)
    - created_after / created_before: ISO datetime range filters for message.created_at
    """
    participant = django_filters.NumberFilter(method='filter_by_participant')
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ['participant', 'created_after', 'created_before']

    def filter_by_participant(self, queryset, name, value):
        # Return messages whose conversation includes the provided participant id
        return queryset.filter(conversation__participants__id=value)
