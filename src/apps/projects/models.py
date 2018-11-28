from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db import models
from utils.choices import EXCERPT_TYPE_CHOICES
from utils.model_mixins import TimestampedMixin


class Theme(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField()
    icon = models.FileField(upload_to='icons/', verbose_name=_('icon'),
                            null=True, blank=True)

    class Meta:
        verbose_name = _('theme')
        verbose_name_plural = _('themes')

    def save(self):
        self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return '%s' % (self.name)


class DocumentType(models.Model):
    title = models.CharField(_('title'), max_length=50)
    initials = models.CharField(_('initials'), max_length=200)

    class Meta:
        verbose_name = _('document type')
        verbose_name_plural = _('document types')

    def __str__(self):
        return '%s' % (self.title)


class Document(TimestampedMixin):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='documents',
                              verbose_name=_('owner'))
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField()
    description = models.TextField(_('description'))
    document_type = models.ForeignKey('projects.DocumentType', blank=True,
                                      null=True, on_delete=models.CASCADE,
                                      verbose_name=_('document type'))
    themes = models.ManyToManyField('projects.Theme', verbose_name=_('themes'))
    number = models.IntegerField(_('number'), blank=True, null=True)
    year = models.IntegerField(_('year'), blank=True, null=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def save(self):
        self.slug = slugify(self.title)
        super().save()

    def __str__(self):
        return '%s' % (self.title)


class Excerpt(models.Model):
    document = models.ForeignKey('projects.Document', on_delete=models.CASCADE,
                                 verbose_name=_('document'),
                                 related_name='excerpts')
    parent = models.ForeignKey('self', related_name='children',
                               verbose_name=_('parent'), null=True, blank=True,
                               on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_('order'), default=0)
    excerpt_type = models.CharField(_('excerpt type'), max_length=200,
                                    choices=EXCERPT_TYPE_CHOICES,
                                    blank=True, null=True)
    number = models.PositiveIntegerField(_('number'), null=True, blank=True)
    content = models.TextField(_('content'))

    class Meta:
        verbose_name = _('excerpt')
        verbose_name_plural = _('excerpts')
        ordering = ('order', )

    def __str__(self):
        return '%s' % (self.content)
