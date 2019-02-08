from django.utils.translation import ugettext_lazy as _
from django import template
from datetime import date
from collections import OrderedDict
import string
from apps.projects.models import Excerpt

register = template.Library()


def int_to_letter(number):
    num2alpha = dict(zip(range(1, 27), string.ascii_lowercase))
    return num2alpha[number]


def int_to_roman(num):

    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])


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


@register.simple_tag()
def excerpt_suggestions(excerpt, user=None):
    suggestions = excerpt.suggestions.all()
    if user:
        suggestions = suggestions.exclude(author=user)
    if suggestions:
        return True
    else:
        return False


@register.simple_tag
def excerpt_numbering(excerpt):
    if excerpt.number and excerpt.excerpt_type:
        type_name = excerpt.excerpt_type.slug
        if type_name == 'artigo':
            if excerpt.number <= 9:
                return "Art. %dº " % excerpt.number
            else:
                return "Art. %d " % excerpt.number
        elif type_name == 'paragrafo':
            if excerpt.number <= 9:
                siblings_count = Excerpt.objects.filter(
                    excerpt_type__slug=excerpt.excerpt_type.slug,
                    parent=excerpt.parent
                ).count()
                if excerpt.number == 1 and siblings_count == 1:
                    return "%s. " % _("Sole paragraph")
                else:
                    return "§ %dº " % excerpt.number
            else:
                return "§ %d " % excerpt.number
        elif type_name == 'inciso':
            return "%s - " % int_to_roman(excerpt.number)
        elif type_name == 'alinea':
            return "%s) " % int_to_letter(excerpt.number)
        elif type_name == 'titulo':
            return "Título %s" % int_to_roman(excerpt.number)
        elif type_name == 'livro':
            return "Livro %s" % int_to_roman(excerpt.number)
        elif type_name == 'capitulo':
            return "Capítulo %s" % int_to_roman(excerpt.number)
        elif type_name == 'secao':
            return "Seção %s" % int_to_roman(excerpt.number)
        elif type_name == 'subsecao':
            return "Subseção %s" % int_to_roman(excerpt.number)
        elif type_name == 'item':
            return "%s." % excerpt.number
        elif type_name == 'citacao':
            return ''
        else:
            return "%s %s" % (excerpt.excerpt_type.name, excerpt.number)
    else:
        return ''


@register.filter()
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter()
def is_open(closing_date):
    if closing_date > date.today():
        is_open = True
    else:
        is_open = False
    return is_open
