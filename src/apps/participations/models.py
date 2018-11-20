from django.utils.translation import ugettext_lazy as _
from django.db import models
from utils.model_mixins import TimestampedMixin
from utils.choices import (OPINION_VOTE_CHOICES, EXCERPT_TYPE_CHOICES,
                           AMENDMENT_TYPE_CHOICES)
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from apps.accounts.models import InvitedEmail


class InvitedGroup(TimestampedMixin):
    document = models.ForeignKey('projects.Document',
                                 on_delete=models.CASCADE,
                                 related_name='invited_groups',
                                 verbose_name=_('document'))
    thematic_group = models.ForeignKey('accounts.ThematicGroup',
                                       on_delete=models.CASCADE,
                                       related_name='invited_groups',
                                       verbose_name=_('thematic group'),
                                       null=True, blank=True)
    closing_date = models.DateField(_('closing date'))
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('invited group')
        verbose_name_plural = _('invited groups')

    def __str__(self):
        if self.thematic_group:
            return '%s <%s>' % (self.document.title,
                                self.thematic_group.owner.email)
        else:
            return '%s <%s>' % (self.document.title, _('public participation'))


class Suggestion(TimestampedMixin):
    invited_group = models.ForeignKey('participations.InvitedGroup',
                                      on_delete=models.CASCADE,
                                      related_name='suggestions',
                                      verbose_name=_('invited group'))
    excerpt = models.ForeignKey('projects.Excerpt',
                                on_delete=models.CASCADE,
                                related_name='suggestions',
                                verbose_name=_('excerpt'))
    start_index = models.PositiveIntegerField(_('start index'))
    end_index = models.PositiveIntegerField(_('end index'))
    content = models.TextField(_('content'))
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                               related_name='suggestions',
                               verbose_name=_('author'))

    class Meta:
        verbose_name = _('suggestion')
        verbose_name_plural = _('suggestions')

    def __str__(self):
        return '%s <%s>' % (self.content,
                            self.author.email)


class OpinionVote(TimestampedMixin):
    suggestion = models.ForeignKey('participations.Suggestion',
                                   on_delete=models.CASCADE,
                                   related_name='votes',
                                   verbose_name=_('suggestion'))
    excerpt = models.ForeignKey('projects.Excerpt',
                                on_delete=models.CASCADE,
                                related_name='votes',
                                verbose_name=_('excerpt'))
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='votes',
                              verbose_name=_('owner'))
    opinion_vote = models.CharField(_('opinion type'), max_length=200,
                                    choices=OPINION_VOTE_CHOICES)

    class Meta:
        verbose_name = _('opinion vote')
        verbose_name_plural = _('opinion votes')

    def __str__(self):
        return '%s <%s>' % (self.owner.email,
                            self.opinion_vote)


class Amendment(TimestampedMixin):
    invited_group = models.ForeignKey('participations.InvitedGroup',
                                      on_delete=models.CASCADE,
                                      related_name='amendments',
                                      verbose_name=_('invited group'))
    excerpt = models.ForeignKey('projects.Excerpt',
                                on_delete=models.CASCADE,
                                related_name='amendments',
                                verbose_name=_('excerpt'))
    content = models.TextField(_('content'))
    amendment_type = models.CharField(_('amendment type'), max_length=200,
                                      choices=AMENDMENT_TYPE_CHOICES)
    excerpt_type = models.CharField(_('excerpt type'), max_length=200,
                                    choices=EXCERPT_TYPE_CHOICES,
                                    blank=True, null=True)
    number = models.PositiveIntegerField(_('number'), null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                               related_name='amendments',
                               verbose_name=_('author'))

    class Meta:
        verbose_name = _('amendment')
        verbose_name_plural = _('amendments')

    def __str__(self):
        return '%s <%s>' % (self.content,
                            self.author.email)


def send_invite(email, document_title, hash):
    html = render_to_string('emails/invite.html', {'title': document_title,
                                                   'hash': hash})
    subject = u'[Wikilegis] Convite para grupo de edição'
    mail = EmailMultiAlternatives(subject, '',
                                  settings.EMAIL_HOST_USER,
                                  [email])
    mail.attach_alternative(html, 'text/html')
    mail.send()


def save_invited_email(sender, instance, **kwargs):
    for participant in instance.thematic_group.participants.all():
        invited_email, created = InvitedEmail.objects.get_or_create(
            group=instance, email=participant.email)
        if created:
            send_invite(participant.email, instance.document.title,
                        invited_email.hash_id)


post_save.connect(save_invited_email, sender=InvitedGroup)
