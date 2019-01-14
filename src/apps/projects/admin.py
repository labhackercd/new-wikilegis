from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from constance import config
from . import camara_deputados
from . import models


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'initials')


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'owner',
        'title',
        'slug',
        'description',
        'document_type',
        'number',
        'year',
    )
    list_filter = ('created', 'modified', 'owner', 'document_type')
    search_fields = ('slug',)
    prepopulated_fields = {'slug': ['title']}
    actions = ['fetch_document_informations']

    def fetch_document_informations(self, request, queryset):
        if config.USE_CD_OPEN_DATA:
            success = 0
            for document in queryset:
                try:
                    camara_deputados.create_document_info(document)
                    success += 1
                except camara_deputados.ProposalNotFound:
                    self.message_user(
                        request,
                        _('Document "{}" not found on Câmara dos Deputados '
                          'API.'.format(document.title)), level='error')

            self.message_user(
                request,
                _('{} document(s) informations was fetched '
                  'successfully.'.format(success)))
        else:
            self.message_user(
                request,
                _('USE_CD_OPEN_DATA config parameter is disabled.'),
                level='warning'
            )
    fetch_document_informations.short_description = _(
        "Fetch documents informations"
    )


@admin.register(models.ExcerptType)
class ExcerptTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'align_center')
    list_filter = ('align_center',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.Excerpt)
class ExcerptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'document',
        'parent',
        'order',
        'excerpt_type',
        'number',
        'content',
    )
    list_filter = ('document', 'parent')


@admin.register(models.DocumentInfo)
class DocumentInfoAdmin(admin.ModelAdmin):
    list_display = (
        'cd_id',
        'document',
        'abridgement',
        'status',
    )
    list_filter = ('document', 'status')


@admin.register(models.DocumentAuthor)
class DocumentAuthorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author_type',
    )
    list_filter = ('author_type', )
