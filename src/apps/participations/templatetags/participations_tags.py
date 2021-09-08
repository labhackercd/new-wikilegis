from django import template
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils import timezone
from apps.participations.models import OpinionVote, Suggestion


register = template.Library()


@register.simple_tag
def highlight_excerpt(excerpt, group, user=None):
    if user:
        if user is not None and user.is_authenticated:
            qs = excerpt.suggestions.filter(author=user, invited_group=group)
        elif not user.is_authenticated:
            return excerpt.content
    else:
        qs = excerpt.suggestions.filter(invited_group=group)

    opening_indexes = {}
    closing_indexes = set()
    for suggestion in qs:
        intersections = qs.filter(Q(
            Q(start_index__gte=suggestion.start_index,
              end_index__lte=suggestion.end_index) |
            Q(start_index__lte=suggestion.start_index,
              end_index__lte=suggestion.end_index,
              end_index__gte=suggestion.start_index) |
            Q(start_index__gte=suggestion.start_index,
              start_index__lte=suggestion.end_index,
              end_index__gte=suggestion.end_index) |
            Q(start_index__lte=suggestion.start_index,
              end_index__gte=suggestion.end_index)
        ))

        ids_list = opening_indexes.get(suggestion.start_index, set())
        ids_list.add(suggestion.id)
        opening_indexes[suggestion.start_index] = ids_list
        closing_indexes.add(suggestion.end_index)

        if intersections.count() > 0:
            indexes = []
            for s, e in intersections.values_list('start_index', 'end_index'):
                indexes.extend([s, e])
            indexes = sorted(list(set(indexes)))

            for i in range(len(indexes) - 1):
                start = indexes[i]
                end = indexes[i + 1]
                ids = list(intersections.filter(
                    start_index__lte=start,
                    end_index__gte=end
                ).values_list('id', flat=True))

                ids_list = opening_indexes.get(start, set())
                ids_list.update(ids)
                opening_indexes[start] = ids_list
                closing_indexes.add(end)

    html = excerpt.content
    length_diff = 0
    closing_indexes = sorted(closing_indexes)
    for index, ids in opening_indexes.items():
        index += length_diff
        span = ('<span class="text-highlight js-highlight" '
                'data-suggestion-ids="{}">'.format(
                    ','.join([str(x) for x in ids])))
        close_span = '</span>'
        close_index = closing_indexes.pop(0) + length_diff
        html = '{prev}{open_span}{content}{close_span}{after}'.format(
            prev=html[:index],
            open_span=span,
            content=html[index:close_index],
            close_span=close_span,
            after=html[close_index:]
        )
        length_diff += len(span)
        length_diff += len(close_span)

    return mark_safe(html)


@register.simple_tag
def highlight_suggestion(suggestion):
    span = '<span class="text-highlight">'
    close_span = '</span>'
    content = suggestion.excerpt.content
    content = '{prev}{open_span}{content}{close_span}{after}'.format(
        prev=content[:suggestion.start_index],
        open_span=span,
        content=content[suggestion.start_index:suggestion.end_index],
        close_span=close_span,
        after=content[suggestion.end_index:]
    )
    return mark_safe(content)


@register.simple_tag
def can_suggest(group, user):
    if user.is_authenticated:
        if group.closing_date >= timezone.now().date():
            return True
        else:
            return False
    else:
        return False


@register.simple_tag
def to_reduce(group, excerpt):
    suggestions_count = excerpt.suggestions.filter(
        id__in=group.suggestions.values_list('id', flat=True)).count()
    if suggestions_count > 0:
        return False
    else:
        if group.suggestions.all():
            return True
        else:
            return False


@register.filter
def count_votes(votes, vote_type):
    return votes.filter(opinion_vote=vote_type).count()


@register.filter
def votes_percent(votes, vote_type):
    total_votes = votes.count()
    votes_by_type = votes.filter(opinion_vote=vote_type).count()
    return int((votes_by_type / total_votes) * 100)


@register.filter
def votes_consensus(votes):
    total = votes.count()
    if total == 0:
        return 0
    else:
        approves = votes.filter(opinion_vote='approve').count()
        neutrals = votes.filter(opinion_vote='neutral').count()
        rejects = votes.filter(opinion_vote='reject').count()
        result = (abs(approves - neutrals) + abs(approves - rejects) +
                  abs(rejects - neutrals)) / (total * 2)
        return int(result * 100)


@register.filter
def majority_votes(votes):
    approves = votes.filter(opinion_vote='approve').count()
    neutrals = votes.filter(opinion_vote='neutral').count()
    rejects = votes.filter(opinion_vote='reject').count()
    if approves > neutrals and approves > rejects:
        return "approves"
    elif rejects > neutrals and rejects > approves:
        return "rejects"
    elif neutrals > rejects and neutrals > approves:
        return "neutrals"
    else:
        return False


@register.filter
def excerpt_participants(excerpt, group):
    excerpt_opinions = excerpt.suggestions.filter(invited_group=group)
    excerpt_author_opinions = excerpt_opinions.values_list(
        'author_id', flat=True)
    opinions_author_votes = OpinionVote.objects.filter(
        suggestion__in=excerpt_opinions).values_list(
        'owner_id', flat=True)
    participants_ids = set(list(excerpt_author_opinions) +
                           list(opinions_author_votes))
    return len(participants_ids)


@register.filter
def group_participants(group):
    group_opinions = Suggestion.objects.filter(invited_group=group)
    group_author_opinions = group_opinions.values_list(
        'author_id', flat=True)
    group_opinions_ids = group_opinions.values_list('id', flat=True)
    group_author_votes = OpinionVote.objects.filter(
        suggestion_id__in=group_opinions_ids).values_list(
        'owner_id', flat=True)
    participants_ids = set(list(group_author_votes) +
                           list(group_author_opinions))
    return len(participants_ids)


@register.filter
def group_votes(group):
    group_opinions = Suggestion.objects.filter(invited_group=group)
    group_opinions_ids = group_opinions.values_list('id', flat=True)
    group_votes_count = OpinionVote.objects.filter(
        suggestion_id__in=group_opinions_ids).count()
    return group_votes_count


@register.filter
def excerpt_opinions(excerpt, group):
    count_opinions = excerpt.suggestions.filter(invited_group=group).count()
    return count_opinions


@register.filter()
def excerpt_votes(excerpt, group):
    votes_list = [suggestion.votes.count()
                  for suggestion in excerpt.suggestions.filter(
                      invited_group=group)]
    return sum(votes_list)


def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0


@register.simple_tag
def relevance_classes(relevance_participations=0,
                      relevance_opinions=0,
                      relevance_votes=0):
    classes = ''
    relevance_participations = to_float(relevance_participations)
    relevance_opinions = to_float(relevance_opinions)
    relevance_votes = to_float(relevance_votes)
    if relevance_participations < 20:
        classes += 'js-participationAmount1'
    elif relevance_participations < 40:
        classes += 'js-participationAmount2'
    elif relevance_participations < 60:
        classes += 'js-participationAmount3'
    elif relevance_participations < 80:
        classes += 'js-participationAmount4'
    elif relevance_participations == 100:
        classes += 'js-participationAmount5'

    if relevance_opinions < 20:
        classes += ' js-opinionsAmount1'
    elif relevance_opinions < 40:
        classes += ' js-opinionsAmount2'
    elif relevance_opinions < 60:
        classes += ' js-opinionsAmount3'
    elif relevance_opinions < 80:
        classes += ' js-opinionsAmount4'
    elif relevance_opinions == 100:
        classes += ' js-opinionsAmount5'

    if relevance_votes < 20:
        classes += ' js-votesAmount1'
    elif relevance_votes < 40:
        classes += ' js-votesAmount2'
    elif relevance_votes < 60:
        classes += ' js-votesAmount3'
    elif relevance_votes < 80:
        classes += ' js-votesAmount4'
    elif relevance_votes == 100:
        classes += ' js-votesAmount5'

    return classes
