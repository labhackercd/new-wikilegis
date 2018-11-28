from django import template
from datetime import date

register = template.Library()


def get_invited_group(document, permission='public', user=None):
    if permission == 'private':
        group = [
            group
            for group in document.invited_groups.filter(is_open=False)
            if user in group.thematic_group.participants.all()
        ][0]
    else:
        group = document.invited_groups.filter(is_open=True).first()
    return group


@register.simple_tag()
def document_is_open(document, permission='public', user=None):
    is_open = False
    group = get_invited_group(document, permission, user)
    if group.closing_date >= date.today():
        is_open = True
    return is_open


@register.simple_tag()
def document_closing_date(document, permission='public', user=None):
    group = get_invited_group(document, permission, user)
    return group.closing_date.strftime('%d/%m/%Y')


@register.simple_tag()
def document_suggestions(document, permission='public', user=None):
    group = get_invited_group(document, permission, user)
    return group.suggestions.count()
