# -*- encoding: utf-8 -*-
from datetime import date, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tarefas.forms import TarefaForm
from tarefas.models import Tarefa
from tarefas.serializers import TarefaSerializer


class TarefaViewSet(viewsets.ModelViewSet):
    """
    Listar, editar, criar e deletar
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Retorna a lista de tarefas do usuário logado e a data atual, junto com as tarefas atrasadas (se o data for hoje)
        """
        user = self.request.user
        # Se não possui data (lista para editar ou excluir)
        if self.request.query_params.get('data') is None:
            lista_tarefas = Tarefa.objects.filter(usuario=user)

        # Se possui data (dia.html)
        else:
            # Recebe a data convertida em date
            data = datetime.strptime(self.request.query_params.get('data', None), '%Y-%m-%d')

            # Lista as tarefas por ordem de prioridade
            lista_tarefas = list(Tarefa.objects.filter(data=data, usuario=user).order_by('prioridade'))

            # Tarefas atrasadas (somente para o dia atual)
            if data.date() == date.today():
                # Recebe as tarefas atrasadas (anteriores a hoje e com status 0)
                tarefas_atrasadas = list(Tarefa.objects.filter(usuario=user, status=0, data__lt=data))

                if tarefas_atrasadas:
                    for x, tarefa in enumerate(tarefas_atrasadas):
                        tarefas_atrasadas[x].status = 2
                    lista_tarefas = lista_tarefas + tarefas_atrasadas

        return lista_tarefas


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
            tarefa.repetida = True
            tarefa.save()
            form.repetir(tarefa)  # método para repetir
            messages.success(self.request, 'Você criou novas tarefas!')
        else:
            form.save()
            messages.success(self.request, 'Você criou uma nova tarefa!')
        return redirect(self.request.META.get('HTTP_REFERER'))

    # todo fazer todo o createview com jquery pois se não apaga as tarefas ao dar form_invalid
    def form_invalid(self, form):
        context = self.get_context_data()
        context['abrir_modal_tarefa'] = 'in'  # Abre o modal boostrap
        return render(self.request, self.request.POST['url'], context)


@login_required()
def buscar_tarefas(request):
    lista_tarefas = Tarefa.objects.filter(usuario=request.user, titulo__icontains=request.GET['s'])
    return render(request, 'busca.html', {'lista_tarefas_busca': lista_tarefas, 'termo_busca': request.GET['s']})


@login_required()
def editar_tarefa(request):
    if request.method == 'GET':
        tarefa = get_object_or_404(Tarefa, id=request.GET['id'], usuario=request.user)
    else:
        form = TarefaForm(request.POST)
        tarefa = form  # Somente para referenciar antes de enviar via Json
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.pk = form.cleaned_data['id']
            tarefa.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect(request.POST['url'].replace(".html", ""))  # retira o .html da {{ url }}
            # return JsonResponse({'mensagem': 'Tarefa concluída com sucesso'}) # Usado via jquery ajax
            # todo criar else com abrir_modal para exibir o model com erro no formulario
            # todo utilizar ajax para submit form, mas como vou atualizar a lista de tarefas (de tal dia ou semana)

    return JsonResponse(
            {'titulo': tarefa.titulo, 'descricao': tarefa.descricao, 'data': tarefa.data, 'hora': tarefa.hora,
             'duracao': tarefa.duracao, 'prioridade': tarefa.prioridade,
             'papel': tarefa.papel, 'projeto': tarefa.projeto, 'usuario': tarefa.usuario.id, 'id': tarefa.id})


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
