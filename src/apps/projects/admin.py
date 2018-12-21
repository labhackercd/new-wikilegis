from django.contrib import admin

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
