from django.contrib import admin
from .models import ParcipantInvitation, OwnerInvitation, PublicAuthorization


@admin.register(ParcipantInvitation)
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


@admin.register(OwnerInvitation)
class OwnerInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'email',
    )
    list_filter = ('created', 'modified')


@admin.register(PublicAuthorization)
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
