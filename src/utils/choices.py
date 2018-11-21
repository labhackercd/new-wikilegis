from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female')),
    ('other', _('Other')),
    ('undisclosed', _('Undisclosed'))
)

UF_CHOICES = (
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MS', 'MS'),
    ('MT', 'MT'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO'),
)

PROFILE_TYPE_CHOICES = (
    ('owner', _('Document Owner')),
    ('defult', _('Default')),
)

EXCERPT_TYPE_CHOICES = (
    ('book', _('Book')),
    ('chapter', _('Chapter')),
    ('title', _('Title')),
    ('section', _('Section')),
    ('subsection', _('Subsection')),
    ('article', _('Article')),
    ('paragraph', _('Paragraph')),
    ('item', _('Item')),
    ('line', _('Line')),
    ('point', _('Point')),
    ('quote', _('Quote')),
)

OPINION_VOTE_CHOICES = (
    ('approve', _('Approve')),
    ('reject', _('Reject')),
    ('neutral', _('Neutral')),
)

AMENDMENT_TYPE_CHOICES = (
    ('additive', _('Additive')),
    ('modifier', _('Modifier')),
    ('supress', _('Supress')),
)
