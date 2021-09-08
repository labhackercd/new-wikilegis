from django.utils.translation import ugettext_lazy as _
from django.db import models
from utils.model_mixins import TimestampedMixin
from utils.choices import OPINION_VOTE_CHOICES, PARTICIPATION_GROUP_CHOICES
from django.urls import reverse


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
    openning_date = models.DateField(_('openning date'), null=True, blank=True)
    closing_date = models.DateField(_('closing date'))
    public_participation = models.BooleanField(_('public participation'),
                                               default=False)
    document_version = models.PositiveIntegerField(default=0)
    text_version = models.PositiveIntegerField(default=0)
    version = models.ForeignKey('projects.DocumentVersion',
                                on_delete=models.CASCADE,
                                verbose_name=_('version'),
                                related_name='invited_groups')
    final_version = models.ForeignKey('projects.DocumentVersion',
                                      on_delete=models.CASCADE,
                                      verbose_name=_('final version'),
                                      related_name='invited_groups_final',
                                      null=True, blank=True)
    group_status = models.CharField(_('group status'), max_length=200,
                                    choices=PARTICIPATION_GROUP_CHOICES,
                                    default='in_progress')

    class Meta:
        verbose_name = _('invited group')
        verbose_name_plural = _('invited groups')

    def get_absolute_url(self):
        return reverse(
            'project', kwargs={'id': self.id,
                               'documment_slug': self.document.slug})

    def get_excerpts(self):
        return self.document.get_excerpts(version=self.version.number)

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
    selected_text = models.TextField(_('selected text'))
    start_index = models.PositiveIntegerField(_('start index'), default=0)
    end_index = models.PositiveIntegerField(_('end index'), default=0)
    content = models.TextField(_('content'))
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                               related_name='suggestions',
                               verbose_name=_('author'))

    class Meta:
        verbose_name = _('suggestion')
        verbose_name_plural = _('suggestions')
        ordering = ('start_index', )

    def votes_count(self, opinion_type=None):
        if opinion_type:
            count_result = self.votes.filter(opinion_vote=opinion_type).count()
        else:
            count_result = self.votes.count()
        return count_result

    def __str__(self):
        return '%s <%s>' % (self.content,
                            self.author.email)


class OpinionVote(TimestampedMixin):
    suggestion = models.ForeignKey('participations.Suggestion',
                                   on_delete=models.CASCADE,
                                   related_name='votes',
                                   verbose_name=_('suggestion'))
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                              related_name='votes',
                              verbose_name=_('owner'))
    opinion_vote = models.CharField(_('opinion type'), max_length=200,
                                    choices=OPINION_VOTE_CHOICES)

    class Meta:
        unique_together = ('suggestion', 'owner')
        verbose_name = _('opinion vote')
        verbose_name_plural = _('opinion votes')

    def __str__(self):
        return '%s <%s>' % (self.owner.email,
                            self.opinion_vote)
