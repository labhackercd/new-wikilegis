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
    list_filter = ('created', 'modified', 'accepted', 'answered')
    search_fields = ('group__thematic_group__name', 'email')
    raw_id_fields = ('group',)


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
    list_filter = ('created', 'modified')
    search_fields = ('group__thematic_group__name',)
    raw_id_fields = ('group', 'congressman')


@admin.register(models.FeedbackAuthorization)
class FeedbackAuthorizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'video_id',
        'hash_id',
        'group',
        'version',
    )
    list_filter = ('created', 'modified')
    raw_id_fields = ('group', 'version')


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
    list_filter = ('created', 'modified', 'was_read')
    search_fields = ('user__first_name',)
    raw_id_fields = ('user',)
