from django.contrib import admin

from .models import InvitedGroup, Suggestion, OpinionVote, Amendment


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
        'document',
        'thematic_group',
        'closing_date',
        'public_participation',
    )


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'invited_group',
        'excerpt',
        'selected_text',
        'content',
        'author',
    )
    list_filter = (
        'created',
        'modified',
        'invited_group',
        'excerpt',
        'author',
    )


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
    list_filter = ('created', 'modified', 'suggestion', 'owner')


@admin.register(Amendment)
class AmendmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'invited_group',
        'excerpt',
        'content',
        'amendment_type',
        'excerpt_type',
        'number',
        'author',
    )
    list_filter = (
        'created',
        'modified',
        'invited_group',
        'excerpt',
        'author',
    )
