from django import forms
from django.forms import ModelForm
from .models import Preaching, Tag
from ckeditor.widgets import CKEditorWidget


class PreachingForm(ModelForm):
    tags = forms.CharField(required = True, max_length=255, widget=forms.HiddenInput)
    class Meta:
        model = Preaching
        fields = ['title', 'text', 'date', 'privacy', 'tags']   
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        
        }

    def clean_tags(self):
        data = self.cleaned_data['tags']
        if data is None:
            raise 
        tags = tuple(Tag.objects.get_or_create(title=tag) for tag in tuple(data.split(',')))
        return tuple([x[0].id for x in list(tags) ])

'''
    def __init__(self, user, *args, **kwargs):
        super(PreachingForm, self).__init__(*args, **kwargs)
        self.user = user
'''

'''
    def save(self):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        date = self.cleaned_data['date']
        privacy = self.cleaned_data['privacy']
        tags = self.cleaned_data['tags']
        print('tags is ' + str(tags))
        preaching = Preaching.objects.create(title=title, text=text, date=date,privacy=privacy, user=self.user)     
        for tag in tags:
            preaching.tags.add(tag.id)
'''