from django.contrib import admin
from .models import Message, MessageHistory, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "timestamp", "read", "edited")
    search_fields = ("sender__username", "receiver__username", "content")

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "edited_at")
    readonly_fields = ("edited_at",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "read")
    list_filter = ("read",)
