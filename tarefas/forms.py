# -*- encoding: utf-8 -*-
from django import forms

__author__ = 'GuiLe Garcia'
from tarefas.models import Tarefa

class TarefaForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(format='%Y/%m/%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%y'])
    repeticao = forms.CharField(max_length=300, required=None)
    num_repeticao = forms.IntegerField(required=None)
    url = forms.CharField(max_length=200, required=None)
    id = forms.CharField(max_length=20, required=None)

    class Meta:
        model = Tarefa
        fields = ('titulo', 'descricao', 'data', 'hora', 'duracao', 'prioridade', 'papel', 'projeto', 'usuario')
