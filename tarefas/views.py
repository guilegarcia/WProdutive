# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
from tarefas.forms import TarefaForm
from tarefas.models import Tarefa
from usuarios.views import LoginRequiredMixin


@login_required()
def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa adicionada com sucesso')
            # todo atualizar lista da session
            # todo criar repetições
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Formulário não é válido!')
            return render(request, request.POST['url'], {'abrir_modal_tarefa': 'in', 'form': form})
    else:
        form = TarefaForm
        return render(request, 'dia.html', {'form': form})


@login_required()
def buscar_tarefas(request):
    lista_tarefas = Tarefa.objects.filter(usuario=request.user, titulo__icontains=request.GET['s'])
    return render(request, 'busca.html', {'lista_tarefas_busca': lista_tarefas, 'termo_busca': request.GET['s']})

@login_required()
def editar_tarefa(request):
    if request.method == 'GET':
        tarefa = get_object_or_404(Tarefa, id=request.GET['id'], usuario=request.user)
        id_tarefa = tarefa.id
        form = TarefaForm(instance=tarefa)
    else:
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.id = form.cleaned_data['id']
            tarefa.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            # todo não está fechando o modal depois de editado
            return redirect(request.META.get('HTTP_REFERER', None) or '/')

    return render(request, request.GET['url'], {'form': form, 'abrir_modal_tarefa': 'in', 'editar_tarefa': True, 'id_tarefa': id_tarefa})

"""
# Usar https://docs.djangoproject.com/en/1.8/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin
class UsuarioUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Tarefa
    fields = ['titulo', 'descricao', 'data', 'hora', 'duracao', 'prioridade', 'papel', 'projeto', 'usuario']
    template_name = 'editar-perfil.html'
    success_message = 'Usuário atualizado com sucesso!'

    # success_url = '/usuarios/editar-perfil/'
"""



@login_required()
def excluir_tarefa(request, id=None):
    tarefa = get_object_or_404(Tarefa, usuario=request.user, id=id)
    tarefa.delete()
    messages.success(request, 'Tarefa excluída com sucesso')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def alterar_status(request):
    # todo redirecionar com json e dar um load no conteúdo da página (usar atributos session)
    if request.is_ajax() or request.method == 'POST':
        tarefa = get_object_or_404(Tarefa, id=request.POST['id'], usuario=request.user)
        if request.POST['estado'] == 'marcado':
            tarefa.status = 1
            tarefa.save()
            mensagem = 'Tarefa concluída com sucesso!'
        else:
            tarefa.status = 0
            tarefa.save()
            mensagem = 'Tarefa reativada!'
    return JsonResponse({'mensagem': mensagem})

