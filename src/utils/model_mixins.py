from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimestampedMixin(models.Model):
    created = models.DateTimeField(_('created'), editable=False,
                                   blank=True, auto_now_add=True)
    modified = models.DateTimeField(_('modified'), editable=False,
                                    blank=True, auto_now=True)

    class Meta:
        abstract = True


class ExcerptMixin(TimestampedMixin):
    document = models.ForeignKey('projects.Document', on_delete=models.CASCADE,
                                 verbose_name=_('document'),
                                 related_name='excerpts')
    order = models.PositiveIntegerField(_('order'), default=0)
    excerpt_type = models.ForeignKey('projects.ExcerptType',
                                     verbose_name=_('excerpt type'),
                                     blank=True, null=True,
                                     on_delete=models.SET_NULL)
    number = models.PositiveIntegerField(_('number'), null=True, blank=True)
    content = models.TextField(_('content'))
    version = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
