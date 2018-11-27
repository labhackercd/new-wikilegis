from django import template
from datetime import date

register = template.Library()


def get_closing_date(document, permission='private', user=None):
    if permission == 'public':
        closing_date = [
            group.closing_date for group in document.groups if group.is_open][0]
    else:
        closing_date = [
            group.closing_date
            for group in document.groups
            if user in group.thematic_group.participants.all()
        ][0]
    return closing_date


@register.simple_tag()
def document_is_open(document, permission='private', user=None):
    is_open = False
    closing_date = get_closing_date(document, permission, user)
    if closing_date <= date.today():
        is_open = True
    return is_open


@register.simple_tag()
def document_closing_date(document, permission='private', user=None):
    closing_date = get_closing_date(document, permission, user)
    return closing_date
