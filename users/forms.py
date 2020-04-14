from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=120) 
    middle_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120)
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'middle_name')

