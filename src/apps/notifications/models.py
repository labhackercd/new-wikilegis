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
