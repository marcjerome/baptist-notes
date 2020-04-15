from django import forms
from django.forms import ModelForm
from .models import Preaching
from ckeditor.widgets import CKEditorWidget


class PreachingForm(ModelForm):
    tags = forms.CharField(max_length=100, required=True)
    class Meta:
        model = Preaching
        fields = ['title', 'text', 'date', 'privacy', 'tags']   
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

