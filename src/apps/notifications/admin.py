from django.contrib import admin
from .models import ParcipantInvitation


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
