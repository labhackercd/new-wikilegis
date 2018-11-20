from django.utils.translation import ugettext_lazy as _
from django.db import models
from utils.choices import GENDER_CHOICES, UF_CHOICES, PROFILE_TYPE_CHOICES
from utils.model_mixins import TimestampedMixin


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile',
                                on_delete=models.CASCADE,
                                verbose_name=_('user'))
    themes = models.ManyToManyField('projects.Theme', blank=True,
                                    verbose_name=_('themes'))
    profile_type = models.CharField(_('profile type'), max_length=200,
                                    choices=PROFILE_TYPE_CHOICES,
                                    default='defult')
    gender = models.CharField(_('gender'), max_length=200,
                              choices=GENDER_CHOICES, blank=True, null=True)
    uf = models.CharField(_('uf'), max_length=2, choices=UF_CHOICES, null=True,
                          blank=True)
    country = models.CharField(_('country'), max_length=200, null=True,
                               blank=True)
    birthdate = models.DateField(_('birthdate'), blank=True, null=True)
    avatar = models.CharField(_('avatar'), max_length=200, null=True,
                              blank=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return '%s <%s>' % (self.user.get_full_name(), self.user.email)


class ThematicGroup(models.Model):
    name = models.CharField(_('name'), max_length=50)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='owner_groups',
                              verbose_name=_('owner'))
    participants = models.ManyToManyField('auth.User', blank=True,
                                          related_name='thematic_groups',
                                          verbose_name=_('participants'))

    class Meta:
        verbose_name = _('thematic group')
        verbose_name_plural = _('thematic groups')

    def __str__(self):
        return '%s <%s>' % (self.name, self.owner.email)


class InvitedEmail(TimestampedMixin):
    email = models.EmailField()
    group = models.ForeignKey('accounts.ThematicGroup',
                              on_delete=models.CASCADE,
                              related_name='invited_emails',
                              verbose_name=_('group'))
    accepted = models.BooleanField(_('accepted'), default=False)

    class Meta:
        unique_together = ('email', 'group')
        verbose_name = _('invited email')
        verbose_name_plural = _('invited emails')

    def __str__(self):
        return '%s' % (self.email)
