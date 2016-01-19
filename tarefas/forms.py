# -*- encoding: utf-8 -*-
import copy
from datetime import timedelta
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

        # Verifica qual é o tipo de repetição
        if data['repeticao'] == 'diario':
            intervalo_dias = 1
        elif data['repeticao'] == 'semanal':
            intervalo_dias = 7
        elif data['repeticao'] == 'mensal':
            intervalo_dias = 28
        else:
            intervalo_dias = 365

        # Cria a tarefa com base no formulario
        tarefa_original = Tarefa(**datas)

        # Faz uma cópia da tarefa original (sem referência)
        tarefa = copy.copy(tarefa_original)

        # todo verificar se esta tarefa tem id (setar repetida=True e adicionar FK nas outras)

        # Cria as tarefas repetidas
        for x in range(1, data['num_repeticao']):
            tarefa.data = tarefa.data + timedelta(days=intervalo_dias)
            tarefa.tarefa_original = tarefa_original
            tarefa.id = None  # Força a adição de uma nova tarefa no DB
            tarefa.save()
