from django import forms
from .models import Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.forms import ModelForm
from .models import Order


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='ФИО', required=True,
                                 help_text='Укажите свое ФИО. Только кирилица, дефис и пробелы.')
    email = forms.EmailField(label='Электронная почта', max_length=254, help_text='Укажите валидную электронную почту',
                             required=True)
    agreement = forms.BooleanField(label='Регистрируясь, вы даете согласие на обработку персональных данных.',
                                   required=True)
    username = forms.CharField(label='Логин', help_text='Должен быть уникальным. Только латиница и дефис',
                               required=True)
    password1 = forms.CharField(label='Введите пароль', required=True,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', required=True,
                                widget=forms.PasswordInput)

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


class NewOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'description', 'category', 'plan']
        plan = forms.ImageField(widget=forms.FileInput, label="Загрузите план вашей квартиры")
