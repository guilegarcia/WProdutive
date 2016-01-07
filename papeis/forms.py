from django import forms

from papeis.models import Papel

__author__ = 'GuiLe Garcia'

class FormPapel(forms.ModelForm):
    class Meta:
        model = Papel
        fields = '__all__'
