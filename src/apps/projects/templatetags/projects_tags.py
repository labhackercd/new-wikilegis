from django import template
from datetime import date

register = template.Library()


def get_closing_date(document, permission='public', user=None):
    if permission == 'private':
        closing_date = [
            group.closing_date
            for group in document.invited_groups.filter(is_open=False)
            if user in group.thematic_group.participants.all()
        ][0]
    else:
        group = document.invited_groups.filter(is_open=True).first()
        closing_date = group.closing_date
    return closing_date


@register.simple_tag()
def document_is_open(document, permission='public', user=None):
    is_open = False
    closing_date = get_closing_date(document, permission, user)
    if closing_date >= date.today():
        is_open = True
    return is_open


@register.simple_tag()
def document_closing_date(document, permission='public', user=None):
    closing_date = get_closing_date(document, permission, user)
    return closing_date.strftime('%d/%m/%Y')
