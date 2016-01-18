# -*- encoding: utf-8 -*-
from django import forms

from tarefas.models import Tarefa

__author__ = 'GuiLe Garcia'


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

    # Cria as tarefas repetidas
    def repeat(self):
        data = self.cleaned_data
        # Copia e limpa os informações extras do form para Tarefa (não consegui fazer direto por ModelForm.save())
        datas = data.copy()
        del datas['repeticao'], datas['num_repeticao'], datas['url']

        # todo verificar se é diário, semanal, mensal ou anual.
        for x in range(1, data['num_repeticao']):
            tarefa = Tarefa(**datas)
            tarefa.id = None
            tarefa.save()

