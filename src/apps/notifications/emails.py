from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site


def get_site_domain():
    site_url = Site.objects.get_current().domain
    return site_url


def send_participant_invitation(email, document_title, hash):
    html = render_to_string('emails/participant_invitation.html',
                            {'title': document_title,
                             'hash': hash,
                             'site_url': get_site_domain()
                             })
    subject = _('[Wikilegis] Edit group invitation')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [email])
    mail.attach_alternative(html, 'text/html')
    mail.send()


def send_owner_invitation(email):
    html = render_to_string('emails/owner_invitation.html',
                            {'site_url': get_site_domain()})
    subject = _('[Wikilegis] Document owner invitation')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [email])
    mail.attach_alternative(html, 'text/html')
    mail.send()


def send_remove_participant(document, participant_email):
    html = render_to_string('emails/remove_participant.html',
                            {'document': document,
                             'site_url': get_site_domain()})
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
    html_authorization = render_to_string(
        'emails/congressman_information.html',
        {'document_owner': public_authorization.group.document.owner,
         'document_title': public_authorization.group.document.title,
         'closing_date': closing_date,
         'hash': public_authorization.hash_id,
         'updated': updated,
         'site_url': get_site_domain()})
    subject_authorization = _('[Wikilegis] Authorization request')
    mail_authorization = EmailMultiAlternatives(
        subject_authorization, '', settings.EMAIL_HOST_USER,
        [public_authorization.congressman.email])
    mail_authorization.attach_alternative(html_authorization, 'text/html')
    mail_authorization.send()

    html_request = render_to_string(
        'emails/participation_request.html',
        {'owner': public_authorization.group.document.owner,
         'congressman': public_authorization.congressman.name,
         'phone': public_authorization.congressman.phone,
         'email': public_authorization.congressman.email,
         'document_title': public_authorization.group.document.title,
         'closing_date': closing_date,
         'hash': public_authorization.hash_id,
         'updated': updated,
         'site_url': get_site_domain()})
    subject_request = _('[Wikilegis] Public participation request')
    mail_request = EmailMultiAlternatives(
        subject_request, '', settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER])
    mail_request.attach_alternative(html_request, 'text/html')
    mail_request.send()


def send_feedback_authorization(feedback_authorization):
    html_authorization = render_to_string(
        'emails/feedback_authorization.html',
        {'document': feedback_authorization.group.document,
         'hash_id': feedback_authorization.hash_id,
         'site_url': get_site_domain()})
    subject_authorization = _('[Wikilegis] Feedback authorization request')
    public_authorization = feedback_authorization.group.authorization_emails.first()  # noqa
    mail_authorization = EmailMultiAlternatives(
        subject_authorization, '', settings.EMAIL_HOST_USER,
        [public_authorization.congressman.email])
    mail_authorization.attach_alternative(html_authorization, 'text/html')
    mail_authorization.send()


def send_owner_closed_participation(public_group, proposal_title):
    html = render_to_string(
        'emails/closed-participation-owner.html',
        {'proposal_title': proposal_title,
         'site_url': get_site_domain()})
    subject = _('[Wikilegis] Closed public participation')
    mail_authorization = EmailMultiAlternatives(
        subject, '', settings.EMAIL_HOST_USER,
        [public_group.document.owner.email])
    mail_authorization.attach_alternative(html, 'text/html')
    mail_authorization.send()


def send_finish_participations(invited_group, proposal_title, user_email):
    html = render_to_string(
        'emails/participant-participation-closed.html',
        {'proposal_title': proposal_title,
         'id_group': invited_group.id,
         'slug': invited_group.document.slug,
         'site_url': get_site_domain()})
    subject = _('[Wikilegis] Finish pulic participation')
    mail = EmailMultiAlternatives(
        subject, '', settings.EMAIL_HOST_USER,
        [user_email])
    mail.attach_alternative(html, 'text/html')
    mail.send()
