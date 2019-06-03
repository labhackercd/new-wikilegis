from django.contrib import admin
from apps.notifications import models


@admin.register(models.ParcipantInvitation)
class ParcipantInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'email',
        'group',
        'accepted',
        'answered',
        'hash_id',
    )
    list_filter = ('created', 'modified', 'group', 'accepted', 'answered')


@admin.register(models.PublicAuthorization)
class PublicAuthorizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'congressman',
        'hash_id',
        'group',
    )
    list_filter = ('created', 'modified', 'group')


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'user',
        'message',
        'was_read',
    )
    list_filter = ('created', 'modified', 'user', 'was_read')
