from django import template

register = template.Library()


@register.filter()
def has_new(notifications):
    if notifications.filter(was_read=False):
        return True
    else:
        return False
