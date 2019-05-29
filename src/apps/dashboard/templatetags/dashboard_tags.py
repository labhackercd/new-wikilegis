from django import template

register = template.Library()


@register.filter('endswith')
def endswith(text, ends):
    if isinstance(text, str):
        return text.endswith(ends)
    return False


@register.simple_tag
def get_percent(value, total):
    if int(total) == 0:
        return 0
    else:
        percent = (int(value) / int(total)) * 100
        return percent
