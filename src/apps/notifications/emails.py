from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_participant_invitation(email, document_title, hash):
    html = render_to_string('emails/participant_invitation.html',
                            {'title': document_title,
                             'hash': hash})
    subject = _('[Wikilegis] Edit group invitation')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [email])
    mail.attach_alternative(html, 'text/html')
    mail.send()


def send_owner_invitation(email):
    html = render_to_string('emails/owner_invitation.html')
    subject = _('[Wikilegis] Document owner invitation')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [email])
    mail.attach_alternative(html, 'text/html')
    mail.send()


def send_public_participation(owner, congressman, phone, email, document):
    html = render_to_string('emails/participation_request.html',
                            {'owner': owner,
                             'congressman': congressman,
                             'phone': phone,
                             'email': email,
                             'document_title': document})
    subject = _('[Wikilegis] Public participation request')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [settings.EMAIL_HOST_USER])
    mail.attach_alternative(html, 'text/html')
    mail.send()


def send_remove_participant(document, participant_email):
    html = render_to_string('emails/remove_participant.html',
                            {'document': document})
    subject = _('[Wikilegis] Participant removed')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [participant_email])
    mail.attach_alternative(html, 'text/html')
    mail.send()


def send_public_authorization(public_authorization, updated=False):
    if updated:
        closing_date = public_authorization.closing_date
    else:
        closing_date = public_authorization.group.closing_date

    html = render_to_string(
        'emails/congressman_authorization.html',
        {'document_owner': public_authorization.group.document.owner,
         'document_title': public_authorization.group.document.title,
         'closing_date': closing_date,
         'hash_id': public_authorization.hash_id,
         'updated': updated})
    subject = _('[Wikilegis] Authorization request')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [public_authorization.congressman_email])
    mail.attach_alternative(html, 'text/html')
    mail.send()
