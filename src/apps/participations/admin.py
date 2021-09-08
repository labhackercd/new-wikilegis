from django.contrib import admin

from .models import InvitedGroup, Suggestion, OpinionVote


@admin.register(InvitedGroup)
class InvitedGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'document',
        'thematic_group',
        'closing_date',
        'public_participation',
    )
    list_filter = (
        'created',
        'modified',
        'closing_date',
        'public_participation',
    )
    search_fields = ('thematic_group__name', 'document__title')
    raw_id_fields = ('document', 'thematic_group', 'version', 'final_version')


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'invited_group',
        'content',
        'author',
    )
    list_filter = (
        'created',
        'modified',
    )
    search_fields = ('invited_group__thematic_group__name',
                     'author__first_name', 'content')
    raw_id_fields = ('invited_group', 'excerpt', 'author')


@admin.register(OpinionVote)
class OpinionVoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'suggestion',
        'owner',
        'opinion_vote',
    )
    list_filter = ('created', 'modified')
    search_fields = ('owner__first_name', 'suggestion__content')
    raw_id_fields = ('suggestion', 'owner')
