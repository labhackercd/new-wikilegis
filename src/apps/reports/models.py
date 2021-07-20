from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.model_mixins import TimestampedMixin


PERIOD_CHOICES = (
    ('daily', _('Daily')),
    ('monthly', _('Monthly')),
    ('yearly', _('Yearly')),
    ('all', _('All the time')),
)


class AnalysisMixin(TimestampedMixin):
    start_date = models.DateField(_('start date'), db_index=True)
    end_date = models.DateField(_('end date'), db_index=True)
    period = models.CharField(_('period'), max_length=200, db_index=True,
                              choices=PERIOD_CHOICES, default='daily')

    class Meta:
        abstract = True


class NewUsersReport(AnalysisMixin):
    new_users = models.IntegerField(_('new users'), null=True, blank=True,
                                    default=0)
    class Meta:
        verbose_name = _('new user')
        verbose_name_plural = _('new users')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class VotesReport(AnalysisMixin):
    votes = models.IntegerField(_('votes'), null=True, blank=True,
                                default=0)
    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class OpinionsReport(AnalysisMixin):
    opinions = models.IntegerField(_('opinions'), null=True, blank=True,
                                   default=0)
    class Meta:
        verbose_name = _('opinion')
        verbose_name_plural = _('opinions')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class DocumentsReport(AnalysisMixin):
    documents = models.IntegerField(_('documents'), null=True, blank=True,
                                    default=0)
    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)


class ParticipantsReport(AnalysisMixin):
    participants = models.IntegerField(_('participants'), null=True,
                                       blank=True, default=0)

    class Meta:
        verbose_name = _('participant')
        verbose_name_plural = _('participants')
        unique_together = ('start_date', 'period')

    def __str__(self):
        return ('{} - {}').format(
            self.start_date.strftime("%d/%m/%Y"), self.period)
