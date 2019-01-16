from django import forms
from apps.projects.models import Document, DocumentType


class DocumentForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        empty_label='Tipo'
    )

    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'number',
                  'year', 'themes', 'owner']
