from django import forms
from notes.models import Note
from ckeditor.widgets import CKEditorWidget


class NoteForm(forms.ModelForm):
    note = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Note
        fields = [
            'title',
            'note',
        ]
