# -*- encoding: utf-8 -*-
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView

from projetos.forms import ProjetoForm
from projetos.models import Projeto
from tarefas.models import Tarefa


@login_required()
def criar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto criado com sucesso')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, request.POST['url'],
                          {'abrir_modal_projeto': 'in', 'form': form})

    else:
        form = ProjetoForm
        return render(request, 'dia.html', {'form': form})


# Projetos.html
@login_required()
def projetos(request):
    lista_projetos = Projeto.objects.filter(usuario=request.user)
    request.session['lista_projetos'] = lista_projetos
    return render(request, 'projetos.html', {'projeto_active': 'active'})


# Projeto.html
@login_required()
def projeto(request, id=None):
    projeto = get_object_or_404(Projeto, usuario=request.user, id=id)
    lista_tarefas = Tarefa.objects.filter(usuario=request.user, projeto=projeto)
    total_duracao = gera_total_duracao(request, lista_tarefas)
    progresso = gera_progresso(request, lista_tarefas)
    return render(request, 'projeto.html',
                  {'projeto': projeto, 'lista_tarefas_projeto': lista_tarefas, 'projeto_active': 'active',
                   'total_duracao': total_duracao, 'progresso': progresso})


@login_required()
def editar_projeto(request):
    if request.method == 'GET':
        projeto = get_object_or_404(Projeto, id=request.GET['id'], usuario=request.user)
        form = ProjetoForm(instance=projeto)
    else:
        form = ProjetoForm(request.POST)
        projeto = form # somente para enviar projeto no response
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.id = form.cleaned_data['id']
            projeto.save()
            messages.success(request, 'Projeto atualizado com sucesso')
            return redirect('projetos')

    return JsonResponse({'nome': projeto.nome, 'descricao': projeto.descricao, 'id': projeto.id})
    # return render(request, 'projetos.html', {'form': form, 'abrir_modal_projeto': 'in', 'editar_projeto': '/projetos/editar/'})


# Remover projeto
@login_required()
def excluir_projeto(request, id=None):
    projeto = get_object_or_404(Projeto, usuario=request.user, id=id)
    projeto.delete()
    messages.success(request, 'Projeto excluído com sucesso')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def gera_total_duracao(request, lista_tarefas):
    total_duracao = timedelta(days=0, hours=0, microseconds=0, milliseconds=0, minutes=0, weeks=0)
    for tarefa in lista_tarefas:
        if tarefa.duracao:
            total_duracao = total_duracao + tarefa.duracao
    return total_duracao


@login_required()
def gera_progresso(request, lista_tarefas):
    tarefas_concluidas = 0
    progresso = 0
    for tarefa in lista_tarefas:
        if tarefa.status == 1:
            tarefas_concluidas = + 1
    if len(lista_tarefas) != 0:
        progresso = (tarefas_concluidas / len(lista_tarefas)) * 100
    return progresso
