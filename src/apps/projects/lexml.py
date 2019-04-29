from apps.projects import models
from bs4 import BeautifulSoup
from collections import Counter


ARTICULATIONS = ['Livro', 'Titulo', 'Capitulo', 'Secao', 'Subsecao',
                 'Artigo', 'Paragrafo', 'Inciso', 'Alinea', 'Item']

RESET_BY_ARTICULATION = {
    'livro': ['titulo', 'capitulo', 'secao', 'subsecao', 'paragrafo',
              'inciso', 'alinea', 'item'],
    'titulo': ['capitulo', 'secao', 'subsecao', 'paragrafo', 'inciso',
               'alinea', 'item'],
    'capitulo': ['secao', 'subsecao', 'paragrafo', 'inciso', 'alinea', 'item'],
    'secao': ['subsecao', 'paragrafo', 'inciso', 'alinea', 'item'],
    'subsecao': ['paragrafo', 'inciso', 'alinea', 'item'],
    'artigo': ['paragrafo', 'inciso', 'alinea', 'item'],
    'paragrafo': ['inciso', 'alinea', 'item'],
    'inciso': ['alinea', 'item'],
    'alinea': ['item'],
    'item': [],
    'continuacao': [],
}

ARTICULATION_COUNTER = Counter()


def roman_to_int(input):
    """ Convert a Roman numeral to an integer. """
    if not isinstance(input, type("")):
        raise TypeError("expected string, got %s" % type(input))

    input = input.upper()
    nums = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    sum = 0
    for i in range(len(input)):
        try:
            value = nums[input[i]]
            # If the next place holds a larger number, this value is negative
            if i + 1 < len(input) and nums[input[i + 1]] > value:
                sum -= value
            else:
                sum += value
        except KeyError:
            raise ValueError('input is not a valid Roman numeral: %s' % input)
    return sum


def create_title(data, parent):
    number = data['Rotulo']
    number = number.replace('Título ', '')
    number = number.replace('Capítulo ', '')
    number = number.replace('Seção ', '')
    number = number.replace('Subseção ', '')
    number = roman_to_int(number.strip())
    return {
        'parent': parent,
        # 'excerpt_type': models.ExcerptType.objects.get(slug='titulo'),
        'number': number,
        'content': data['NomeAgrupador'],
    }


def create_excerpt(excerpt_type, data, parent=None, order=0):
    if excerpt_type == 'Livro':
        print('Livro')
        return create_title(data, parent)
    elif excerpt_type == 'Titulo':
        print('Titulo')
        return create_title(data, parent)
    elif excerpt_type == 'Capitulo':
        print('Capitulo')
        return create_title(data, parent)
    elif excerpt_type == 'Secao':
        print('Secao')
        return create_title(data, parent)
    elif excerpt_type == 'Subsecao':
        print('Subsecao')
        return create_title(data, parent)
    elif excerpt_type == 'Artigo':
        print('Artigo')
    elif excerpt_type == 'Paragrafo':
        print('Paragrafo')
    elif excerpt_type == 'Inciso':
        print('Inciso')
    elif excerpt_type == 'Alinea':
        print('Alinea')
    elif excerpt_type == 'Item':
        print('Item')
    else:
        print('Citacao')


# def parse_node(excerpt_type, data, parent=None, order=0):
#     node_data = create_excerpt(excerpt_type, data, parent, order)
#     print(order)
#     for key, value in data.items():
#         if key in ARTICULATIONS:
#             if type(value) != list:
#                 value = [value]
#             for child in value:
#                 order = parse_node(key, child, order=order + 1)

#             if 'Caput' in data.keys():
#                 order = parse_node(key, data['Caput'], order=order + 1)
#     return order

# def parse_lexml(lexml):
#     data = xmltodict.parse(lexml)['Articulacao']
#     for key, value in data.items():
#         if key in ARTICULATIONS:
#             if type(value) != list:
#                 value = [value]
#             for node in value:
#                 parse_node(key, node)

def parse_html(html, document):
    soup = BeautifulSoup(html, features='html.parser')
    excerpts = soup.findAll('p')
    for order, excerpt in enumerate(excerpts):
        excerpt_type = excerpt.attrs['data-tipo']
        number = ARTICULATION_COUNTER[excerpt_type] + 1
        content = excerpt.text
        ARTICULATION_COUNTER.update([excerpt_type])
        print(excerpt_type)
        models.Excerpt.objects.create(
            document=document,
            order=order,
            excerpt_type=models.ExcerptType.objects.get(slug=excerpt_type),
            number=number,
            content=content
        )

        for resetable in RESET_BY_ARTICULATION[excerpt_type]:
            ARTICULATION_COUNTER[resetable] = 0
