# -*- encoding: utf-8 -*-
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from papeis.forms import FormPapel
from papeis.models import Papel
from tarefas.models import Tarefa


@login_required()
def criar_papel(request):
    if request.method == 'POST':
        form = FormPapel(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Papel adicionado com sucesso!')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, request.POST['url'], {'form': form, 'abrir_modal_papel': 'in'})
    else:
        form = FormPapel
        return render(request, 'dia.html', {'form': form})


# Papeis.html
@login_required()
def papeis(request):
    lista_papeis = Papel.objects.filter(usuario=request.user)
    request.session['lista_papeis'] = lista_papeis
    return render(request, 'papeis.html', {'papel_active': 'active'})

@login_required()
def excluir_papel(request, id=None):
    papel = get_object_or_404(Papel, usuario=request.user, id=id)
    papel.delete()
    messages.success(request, 'Papel foi excluído com sucesso')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def editar_papel(request):
    if request.method == 'GET':
        papel = get_object_or_404(Papel, id=request.GET['id'], usuario=request.user)
        form = FormPapel(instance=papel)
    else:
        form = FormPapel(request.POST)
        if form.is_valid():
            papel = form.save(commit=False)
            papel.id = form.cleaned_data['id']
            papel.save()
            messages.success(request, 'Papel atualizado com sucesso')
            return redirect('/papeis/')
    return render(request, 'papeis.html',
              {'form': form, 'abrir_modal_papel': 'in', 'editar_papel': 'true'})


@login_required()
def papel(request, id=None):
    papel = get_object_or_404(Papel, usuario=request.user, id=id)
    lista_tarefas = Tarefa.objects.filter(usuario=request.user, papel=papel)
    total_duracao = gera_total_duracao(request, lista_tarefas)
    return render(request, 'papel.html',
                  {'papel': papel, 'lista_tarefas_papel': lista_tarefas, 'papel_active': 'active',
                   'total_duracao': total_duracao})

@login_required()
def gera_total_duracao(request, lista_tarefas):
    total_duracao = timedelta(days=0, hours=0, microseconds=0, milliseconds=0, minutes=0, weeks=0)
    for tarefa in lista_tarefas:
        if tarefa.duracao:
            total_duracao = total_duracao + tarefa.duracao
    return total_duracao