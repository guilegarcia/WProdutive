# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from tarefas.forms import TarefaForm
from tarefas.models import Tarefa


@method_decorator(login_required, name='dispatch')
class TarefaCreate(SuccessMessageMixin, CreateView):
    """
    Cria a tarefa e suas repetições
    """
    form_class = TarefaForm
    template_name = 'includes/modals.html'

    def form_valid(self, form):
        # Verifica se possui repetições
        if form.cleaned_data['repeticao']:
            # Chama o método para repetir tarefa
            tarefa = form.save(commit=False)
            form.repeat()  # método para repetir
            tarefa.repetida = True
            tarefa.save()
            messages.success(self.request, 'Você criou novas tarefas!')
        else:
            messages.success(self.request, 'Você criou uma nova tarefa!')
        return redirect(self.request.META.get('HTTP_REFERER'))

    # todo fazer todo o createview com jquery pois se não apaga as tarefas ao dar form_invalid
    def form_invalid(self, form):
        context = self.get_context_data()
        context['abrir_modal_tarefa'] = 'in' # Abre o modal boostrap
        return render(self.request, self.request.POST['url'], context)


@login_required()
def buscar_tarefas(request):
    lista_tarefas = Tarefa.objects.filter(usuario=request.user, titulo__icontains=request.GET['s'])
    return render(request, 'busca.html', {'lista_tarefas_busca': lista_tarefas, 'termo_busca': request.GET['s']})


@login_required()
def editar_tarefa(request):
    if request.method == 'GET':
        tarefa = get_object_or_404(Tarefa, id=request.GET['id'], usuario=request.user)
        form = TarefaForm(instance=tarefa)
    else:
        form = TarefaForm(request.POST)
        tarefa = form  # Somente para referenciar antes de enviar via Json
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.id = form.cleaned_data['id']
            tarefa.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect(request.POST['redirect'])
            # todo criar else com abrir_modal para exibir o model com erro no formulario
            # todo inserir o redirect no form do modals.html
            # todo ou fazer por Ajax (melhor maneira) clica > abre modal > envia form * mas se for invalid? *else render (abrir_modal)

    # return render(request, request.GET['url'],
    #               {'form': form, 'abrir_modal_tarefa': 'in', 'editar_tarefa': True, 'id_tarefa': id_tarefa})
    return JsonResponse(
            {'titulo': tarefa.titulo, 'descricao': tarefa.descricao, 'data': tarefa.data, 'hora': tarefa.hora,
             'duracao': tarefa.duracao, 'prioridade': tarefa.prioridade,
             'papel': tarefa.papel, 'projeto': tarefa.projeto, 'usuario.id': tarefa.usuario.id, 'id': tarefa.id})


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
            mensagem = 'Parabéns! Você concluiu mais uma tarefa!'
        else:
            tarefa.status = 0
            tarefa.save()
            mensagem = 'Tarefa reativada!'
    return JsonResponse({'mensagem': mensagem})
