from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from constance import config
from . import models, forms, camara_deputados, import_document


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'initials')


@admin.register(models.DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'name', 'number', 'created', 'auto_save')
    list_filter = ('document',)


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'description',
        'created',
        'modified',
    )
    list_filter = ('created', 'modified', 'owner', 'document_type')
    search_fields = ('slug',)
    prepopulated_fields = {'slug': ['title']}
    actions = ['fetch_document_informations']
    form = forms.DocumentAdminForm

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

    def save_form(self, request, form, change):
        document = form.save(commit=False)
        try:
            import_document.import_txt(form.files['file_txt'], document.id)
        except KeyError:
            pass
        return form.save(commit=False)


@admin.register(models.DocumentVideo)
class DocumentVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'title', 'video_id')
    list_filter = ('document',)


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
        'order',
        'excerpt_type',
        'number',
        'content',
        'version',
    )
    list_filter = ('document', 'version', 'created', 'modified',)


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


@admin.register(models.DocumentAuthorInfo)
class DocumentAuthorInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'cd_id',
        'image_url',
        'party_initials',
        'uf',
    )
    list_filter = ('author',)
