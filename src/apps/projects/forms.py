from django import forms
from apps.projects.models import Document, DocumentType
from django.utils.translation import ugettext_lazy as _


class DocumentForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        empty_label='Tipo',
        required=False
    )

    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'number',
                  'year', 'themes', 'owner']


class DocumentAdminForm(forms.ModelForm):
    file_txt = forms.FileField(label=_('File in txt format'), required=False)

    class Meta:
        model = Document
        fields = ['title', 'slug', 'description', 'document_type', 'number',
                  'year', 'themes', 'owner']
