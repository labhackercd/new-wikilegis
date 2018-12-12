from django import forms
from apps.projects.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'number',
                  'year', 'themes']
