from django.contrib import admin
from .models import ParcipantInvitation, OwnerInvitation


@admin.register(ParcipantInvitation)
class ParcipantInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'email',
        'group',
        'accepted',
        'hash_id',
    )
    list_filter = ('created', 'modified', 'group', 'accepted')


@admin.register(OwnerInvitation)
class OwnerInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'email',
    )
    list_filter = ('created', 'modified')
