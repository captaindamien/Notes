from django.forms import ModelForm, DateInput
from notes.models import Note
from django import forms


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'note',
        ]
