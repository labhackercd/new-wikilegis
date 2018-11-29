from django import template
from django.db.models import Q
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def highlight_suggestions(excerpt):
    qs = excerpt.suggestions.all()
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
            indexes = sorted(indexes)

            for i in range(len(indexes) - 1):
                start = indexes[i]
                end = indexes[i + 1]
                print(start, end)
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
