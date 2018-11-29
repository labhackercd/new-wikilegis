from django.contrib import admin

from .models import Theme, DocumentType, Document, Excerpt, ExcerptType


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'initials')


@admin.register(Document)
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


@admin.register(ExcerptType)
class ExcerptTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'align_center')
    list_filter = ('align_center',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Excerpt)
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
