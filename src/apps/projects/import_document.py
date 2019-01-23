from django.template.defaultfilters import slugify
from apps.projects.models import Excerpt, ExcerptType
import re
import roman
import string


def create_excerpt(type_id, order, document_id, number, content):
    excerpts = Excerpt.objects.filter(document_id=document_id)
    excerpt = Excerpt()
    excerpt.order = order
    excerpt.document_id = document_id
    excerpt.excerpt_type_id = type_id
    if type_id == ExcerptType.objects.get(slug="paragrafo").id:
        type_parent = ExcerptType.objects.get(slug="artigo").id
        excerpt.parent = excerpts.filter(order__lt=order,
                                         excerpt_type_id=type_parent).last()
    elif type_id == ExcerptType.objects.get(slug="inciso").id:
        type_parents = []
        type_parents.append(ExcerptType.objects.get(slug="artigo").id)
        type_parents.append(ExcerptType.objects.get(slug="paragrafo").id)
        excerpt.parent = excerpts.filter(order__lt=order,
                                         excerpt_type__in=type_parents).last()
    elif type_id == ExcerptType.objects.get(slug="alinea").id:
        type_parents = []
        type_parents.append(ExcerptType.objects.get(slug="inciso").id)
        type_parents.append(ExcerptType.objects.get(slug="paragrafo").id)
        excerpt.parent = excerpts.filter(order__lt=order,
                                         excerpt_type__in=type_parents).last()
    elif type_id == ExcerptType.objects.get(slug="item").id:
        type_parent = ExcerptType.objects.get(slug="alinea").id
        excerpt.parent = excerpts.filter(order__lt=order,
                                         excerpt_type_id=type_parent).last()
    elif type_id == ExcerptType.objects.get(slug="citacao").id:
        excerpt.parent = excerpts.exclude(
            excerpt_type_id=type_id).filter(order__lt=order).last()
    excerpt.number = number
    excerpt.content = content
    excerpt.save()


def import_txt(document_txt, document_id):
    response = document_txt.read().decode('utf-8')
    lines = response.splitlines()
    order = 1
    is_quote = False
    for line in lines:
        type_id = None
        if re.match("^\"", line) or is_quote:
            type_id = ExcerptType.objects.get(slug="citacao").id
            content = line
            number = None
            if line.endswith('"'):
                is_quote = False
            elif line.endswith('(NR)'):
                is_quote = False
            else:
                is_quote = True
        elif slugify(line).startswith('livro') and not is_quote:
            type_id = ExcerptType.objects.get(slug="livro").id
            number = roman.fromRoman(
                re.sub("^Livro ", '', line)
            )
            content = lines[order]
        elif slugify(line).startswith('titulo') and not is_quote:
            type_id = ExcerptType.objects.get(slug="titulo").id
            number = roman.fromRoman(
                re.sub("^T\xc3\xadtulo ", '', line)
            )
            content = lines[order]
        elif slugify(line).startswith('capitulo') and not is_quote:
            type_id = ExcerptType.objects.get(slug="capitulo").id
            number = roman.fromRoman(
                re.sub("^CAP\xc3\x8dTULO ", '', line)
            )
            content = lines[order]
        elif slugify(line).startswith('secao') and not is_quote:
            type_id = ExcerptType.objects.get(slug="secao").id
            number = roman.fromRoman(
                re.sub("^Se\xc3\xa7\xc3\xa3o ", '', line)
            )
            content = lines[order]
        elif slugify(line).startswith('subsecao') and not is_quote:
            type_id = ExcerptType.objects.get(slug="subsecao").id
            number = roman.fromRoman(
                re.sub("^Subse\xc3\xa7\xc3\xa3o ", '', line)
            )
            content = lines[order]
        elif (re.match("^Art\. \d+ º", line) or
              re.match("^Art\. \d+\.", line) and not is_quote):
            try:
                label = re.match("^Art\. \d+ º", line).group(0)
            except:
                label = re.match("^Art\. \d+\.", line).group(0)
            type_id = ExcerptType.objects.get(slug="artigo").id
            number = re.search('\d+', label).group(0)
            content = line.replace(label, '')
        elif re.match("^§ \d+º", line) and not is_quote:
            label = re.match("^§ \d+º", line).group(0)
            type_id = ExcerptType.objects.get(slug="paragrafo").id
            number = re.search('\d+', label).group(0)
            content = line.replace(label, '')
        elif slugify(line).startswith('paragrafo-unico') and not is_quote:
            excerpt_type_id = ExcerptType.objects.get(slug="paragrafo").id
            type_id = excerpt_type_id
            number = 1
            content = line.replace('Parágrafo único. ', '')
        elif re.match("^[A-Z\d]+ \W+ ", line) and not is_quote:
            label = re.match("^[A-Z\d]+ \W+ ", line).group(0)
            type_id = ExcerptType.objects.get(slug="inciso").id
            number = roman.fromRoman(
                re.search("^[A-Z\d]+", line).group(0)
            )
            content = line.replace(label, '')
        elif re.match("^[a-z]\W ", line) and not is_quote:
            label = re.match("^[a-z]\W ", line).group(0)
            type_id = ExcerptType.objects.get(slug="alinea").id
            number = string.ascii_lowercase.index(
                re.search("^[a-z]", line).group(0)) + 1
            content = line.replace(label, '')
        elif re.match("^\d+\. ", line) and not is_quote:
            label = re.match("^\d+\. ", line).group(0)
            type_id = ExcerptType.objects.get(slug="item").id
            number = re.search("^\d+", line).group(0)
            content = line.replace(label, '')
        elif line.startswith('Pena') and not is_quote:
            type_id = ExcerptType.objects.get(slug="citacao").id
            content = line
            number = None
        else:
            if (not slugify(lines[order - 2]).startswith('livro') and not
                    slugify(lines[order - 2]).startswith('titulo') and not
                    slugify(lines[order - 2]).startswith('capitulo') and not
                    slugify(lines[order - 2]).startswith('secao') and not
                    slugify(lines[order - 2]).startswith('subsecao')):
                type_id = ExcerptType.objects.get(slug="citacao").id
                content = line
                number = None
        if type_id:
            create_excerpt(type_id, order, document_id, number, content)

        order += 1
