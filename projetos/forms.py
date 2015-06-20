__author__ = 'GuiLe Garcia'
from django import forms
from projetos.models import Projeto


class ProjetoForm(forms.ModelForm):
    url = forms.CharField(max_length=200)
    id = forms.CharField(max_length=20, required=None)

    class Meta:
        model = Projeto
        fields = "__all__"

