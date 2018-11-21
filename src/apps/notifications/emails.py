from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_invite(email, document_title, hash):
    html = render_to_string('emails/invite.html', {'title': document_title,
                                                   'hash': hash})
    subject = _('[Wikilegis] Edit group invitation')
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [email])
    mail.attach_alternative(html, 'text/html')
    mail.send()