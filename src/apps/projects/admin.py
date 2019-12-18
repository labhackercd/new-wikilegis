from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from constance import config
from . import models, forms, camara_deputados, import_document


class VideoInline(admin.TabularInline):
    model = models.DocumentVideo
    verbose_name_plural = _('videos')
    extra = 0


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'initials')
    search_fields = ('title', 'initials')


@admin.register(models.DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'name', 'number', 'created', 'auto_save',
                    'parent')
    search_fields = ('document__title', 'number', 'name')


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'description',
        'created',
        'modified',
    )
    list_filter = ('created', 'modified', 'document_type')
    search_fields = ('slug', 'owner__username', 'title')
    prepopulated_fields = {'slug': ['title']}
    actions = ['fetch_document_informations']
    form = forms.DocumentAdminForm
    inlines = (VideoInline, )

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
    list_filter = ('created', 'modified')
    search_fields = ('document__title', 'version__number', 'version__name')


@admin.register(models.DocumentInfo)
class DocumentInfoAdmin(admin.ModelAdmin):
    list_display = (
        'cd_id',
        'document',
        'abridgement',
        'status',
    )
    list_filter = ('status', )
    search_fields = ('document__title', )


@admin.register(models.DocumentAuthor)
class DocumentAuthorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author_type',
    )
    list_filter = ('author_type', )
    search_fields = ('author_type', 'name')


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


@admin.register(models.DocumentResponsible)
class DocumentResponsibleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'cd_id',
        'image_url',
        'party_initials',
        'uf',
        'email',
        'phone',
    )
    search_fields = ('name',)
