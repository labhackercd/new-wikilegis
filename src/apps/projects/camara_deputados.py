from constance import config
from urllib import parse
from apps.projects.models import (DocumentInfo, DocumentAuthor,
                                  DocumentAuthorInfo)
import requests
import os


class ProposalNotFound(BaseException):
    pass


def make_request(path, params=None):
    headers = {'accept': 'application/json'}
    response = requests.get(
        parse.urljoin(os.path.join(config.CD_OPEN_DATA_URL, ''), path),
        headers=headers,
        params=params,
    )
    return response.json()['dados']


def get_proposal_data(document_type, number, year):
    params = {
        'siglaTipo': document_type,
        'numero': number,
        'ano': year
    }
    data = make_request('proposicoes', params)
    if len(data) == 0:
        raise ProposalNotFound()
    else:
        proposal_id = data[0]['id']
        proposal_data = make_request('proposicoes/{}'.format(proposal_id))

        return proposal_data


def get_authors(proposal_id):
    authors_data = make_request('proposicoes/{}/autores'.format(proposal_id))
    return authors_data


def get_author_info(url_author):
    headers = {'accept': 'application/json'}
    response = requests.get(url_author, headers=headers)
    return response.json()['dados']


def create_document_info(document):
    data = get_proposal_data(
        document.document_type.initials,
        document.number,
        document.year,
    )
    infos = DocumentInfo.objects.get_or_create(document=document)[0]
    infos.abridgement = data['ementa']
    infos.cd_id = data['id']
    infos.keywords = data['keywords']
    infos.legislative_body = data['statusProposicao']['siglaOrgao']
    infos.status = data['statusProposicao']['descricaoSituacao']
    infos.save()

    for author_data in get_authors(infos.cd_id):
        author = DocumentAuthor.objects.get_or_create(
            name=author_data['nome'],
            author_type=author_data['tipo']
        )[0]
        author_info_data = get_author_info(author_data['uri'])
        author_info = DocumentAuthorInfo.objects.get_or_create(
            author=author)[0]
        author_info.cd_id = author_info_data['id']
        author_info.image_url = author_info_data['ultimoStatus']['urlFoto']
        author_info.party_initials = author_info_data['ultimoStatus']['siglaPartido']  # noqa
        author_info.uf = author_info_data['ultimoStatus']['siglaUf']
        author_info.save()

        infos.authors.add(author)
