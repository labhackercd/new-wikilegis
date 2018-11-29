from django import template
from datetime import date

register = template.Library()


def get_invited_group(document, permission='public', user=None):
    if permission == 'private':
        groups = document.invited_groups.filter(public_participation=False)
        group = [
            group
            for group in groups
            if user in group.thematic_group.participants.all()
        ][0]
    else:
        group = document.invited_groups.filter(
            public_participation=True
        ).first()
    return group


@register.simple_tag()
def document_is_open(document, permission='public', user=None):
    public_participation = False
    group = get_invited_group(document, permission, user)
    if group.closing_date >= date.today():
        public_participation = True
    return public_participation


@register.simple_tag()
def document_closing_date(document, permission='public', user=None):
    group = get_invited_group(document, permission, user)
    return group.closing_date.strftime('%d/%m/%Y')


@register.simple_tag()
def document_suggestions(document, permission='public', user=None):
    group = get_invited_group(document, permission, user)
    return group.suggestions.count()
