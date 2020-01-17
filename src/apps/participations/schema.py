import graphene
from graphene_django import DjangoObjectType

from apps.participations.models import Suggestion, OpinionVote


class SuggestionType(DjangoObjectType):
    class Meta:
        model = Suggestion


class OpinionVoteType(DjangoObjectType):
    class Meta:
        model = OpinionVote


class Query(graphene.ObjectType):
    suggestions = graphene.List(SuggestionType)
    votes = graphene.List(OpinionVoteType)

    def resolve_suggestions(self, info, **kwargs):
        return Suggestion.objects.filter(
            invited_group__public_participation=True)

    def resolve_votes(self, info, **kwargs):
        public_suggestions = Suggestion.objects.filter(
            invited_group__public_participation=True
            ).values_list('id', flat=True)
        return OpinionVote.objects.filter(suggestion_id__in=public_suggestions)
