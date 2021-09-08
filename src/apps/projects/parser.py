from apps.projects.models import Excerpt, ExcerptType
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


def parse_html(html, version, document):
    ARTICULATION_COUNTER = Counter()
    soup = BeautifulSoup(html, features='html.parser')
    excerpts = soup.findAll('p')
    for order, excerpt in enumerate(excerpts):
        excerpt_type = excerpt.attrs['data-tipo']
        number = ARTICULATION_COUNTER[excerpt_type] + 1
        content = excerpt.text

        if content.strip() != '':
            ARTICULATION_COUNTER.update([excerpt_type])

            Excerpt.objects.create(
                document=document,
                order=order,
                excerpt_type=ExcerptType.objects.get(slug=excerpt_type),
                number=number,
                content=content,
                version=version
            )

            for resetable in RESET_BY_ARTICULATION[excerpt_type]:
                ARTICULATION_COUNTER[resetable] = 0
