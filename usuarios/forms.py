from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, PasswordInput

__author__ = 'GuiLe Garcia'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password')
        # Adiciona as classes e placeholder no css
        widgets = {
            'first_name': TextInput(attrs={'class': u'form-control', 'placeholder':'Escreva seu nome..'}),
            'username': TextInput(attrs={'class': u'form-control', 'placeholder':'Escreva seu usuario..'}),
            'email': EmailInput(attrs={'class': u'form-control', 'placeholder':'Escreva seu email..'}),
            'password': PasswordInput(attrs={'class': u'form-control', 'placeholder':'Escreva sua senha..'})
        }