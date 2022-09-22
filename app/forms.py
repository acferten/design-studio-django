from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        for letter in re.findall(r'.', data):
            if not ((re.search('[а-яА-Я]', letter)) or (letter == ' ') or (letter == '-')):
                raise forms.ValidationError('ФИО может содержать только кириллицу, дефис и пробелы')
                break

        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        for letter in re.findall(r'.', data):
            if not ((re.search('[a-zA-z]', letter)) or (letter == '-')):
                raise forms.ValidationError('Логин может содержать только латиницу и дефис')
                break
        return data
