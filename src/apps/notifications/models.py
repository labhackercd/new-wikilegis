from django.utils.translation import ugettext_lazy as _
from django.db import models
from utils.model_mixins import TimestampedMixin
import uuid


class ParcipantInvitation(TimestampedMixin):
    email = models.EmailField()
    hash_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey('participations.InvitedGroup',
                              on_delete=models.CASCADE,
                              related_name='invited_emails',
                              verbose_name=_('group'))
    accepted = models.BooleanField(_('accepted'), default=False)
    answered = models.BooleanField(_('answered'), default=False)

    class Meta:
        unique_together = ('email', 'group')
        verbose_name = _('participant invitation')
        verbose_name_plural = _('participant invitations')

    def __str__(self):
        return '%s' % (self.email)


class OwnerInvitation(TimestampedMixin):
    email = models.EmailField()

    class Meta:
        verbose_name = _('owner invitation')
        verbose_name_plural = _('owner invitations')

    def __str__(self):
        return '%s' % (self.email)


class PublicAuthorization(TimestampedMixin):
    congressman = models.ForeignKey('projects.DocumentResponsible',
                                    on_delete=models.CASCADE,
                                    related_name='authorizations',
                                    verbose_name=_('congressman'),
                                    blank=True, null=True)
    hash_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey('participations.InvitedGroup',
                              on_delete=models.CASCADE,
                              related_name='authorization_emails',
                              verbose_name=_('group'))
    closing_date = models.DateField(_('closing date'), null=True, blank=True)

    class Meta:
        verbose_name = _('public authorization')
        verbose_name_plural = _('public authorization')

    def __str__(self):
        return '%s' % (self.congressman.name)


class FeedbackAuthorization(TimestampedMixin):
    video_id = models.CharField(_('video id'), max_length=50)
    hash_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey('participations.InvitedGroup',
                              on_delete=models.CASCADE,
                              related_name='feedback_authorizations',
                              verbose_name=_('group'))
    version = models.ForeignKey('projects.DocumentVersion',
                                on_delete=models.CASCADE,
                                verbose_name=_('version'),
                                related_name='feedback_authorizations')

    class Meta:
        verbose_name = _('feedback authorization')
        verbose_name_plural = _('feedback authorization')

    def __str__(self):
        return '%s' % (self.group.document.slug)


class Notification(TimestampedMixin):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             related_name='notifications',
                             verbose_name=_('user'))
    message = models.TextField()
    was_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')

    def __str__(self):
        return '%s' % (self.user.get_full_name())
