# -*- encoding: utf-8 -*-
from datetime import date, datetime, timedelta
import copy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from tarefas.forms import TarefaForm
from tarefas.models import Tarefa
from tarefas.serializers import TarefaSerializer


class TarefaMixin(object):
    """
    Adiciona as propriedades da Tarefa para serem herdadas pelas classes
    """
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = (IsAuthenticated,)

    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument. Adicionar o "total_duracao" no Json
        """
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'total_duracao': self.total_duracao
        }


class TarefaJSONRenderer(JSONRenderer):
    """
    Adiciona o total_duracao no Json
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'tarefas': data,
                'total_duracao': str(renderer_context['total_duracao'])}  # total_duracao convertido para string
        return super(TarefaJSONRenderer, self).render(data, accepted_media_type, renderer_context)


class TarefaViewSet(TarefaMixin, viewsets.ModelViewSet):
    """
    Listar, editar, criar e deletar
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    renderer_classes = (TarefaJSONRenderer,)

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
                # Recebe as tarefas atrasadas (anteriores a hoje e com status 0) * cria uma copy para não salvar status=2 no DB
                tarefas_atrasadas = copy.copy(list(Tarefa.objects.filter(usuario=user, status=0, data__lt=data)))

                if tarefas_atrasadas:
                    for x, tarefa in enumerate(tarefas_atrasadas):
                        tarefas_atrasadas[x].status = 2
                    lista_tarefas = lista_tarefas + tarefas_atrasadas

        # Adiciona o total duração
        self.total_duracao = gera_total_duracao(lista_tarefas)
        return lista_tarefas


class TarefaSemanaJSONRenderer(JSONRenderer):
    """
    Adiciona o total_duracao no Json da semana
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Recebe uma lista de datetime e transforma em string (para ir para o Json)
        lista_duracao = renderer_context['total_duracao']
        lista_duracao_dias = []
        for duracao_dia in lista_duracao:
            lista_duracao_dias.append(str(duracao_dia))

        data = {'tarefas': data,
                'total_duracao': lista_duracao_dias}
        return super(TarefaSemanaJSONRenderer, self).render(data, accepted_media_type, renderer_context)


class TarefaSemana(TarefaMixin, mixins.ListModelMixin, generics.GenericAPIView):
    """
    Retorna a lista de tarefas de toda a semana (inicio e fim)
    """
    renderer_classes = (TarefaSemanaJSONRenderer,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        data_inicio = datetime.strptime(self.request.query_params.get('inicio', None), '%Y-%m-%d')
        data_fim = datetime.strptime(self.request.query_params.get('fim', None), '%Y-%m-%d')

        lista_tarefas = Tarefa.objects.filter(Q(data__gte=data_inicio) & Q(data__lte=data_fim),
                                              usuario=user)  # gte = maior ou igual e lte = menor ou igual

        # ___ Total horas de cada dia da semana
        self.total_duracao = []
        if lista_tarefas:
            lista_tarefas_aux = []
            data_aux = data_inicio

            # Percorre os 7 dias e cria uma lista de tarefas para cada dia, depois gera lista de duração e acrescenta na lista
            for x in range(0, 7):
                for tarefa in lista_tarefas:
                    if tarefa.data == data_aux.date():
                        # Adiciona a tarefa na lista de tarefas deste dia
                        lista_tarefas_aux.append(tarefa)
                # Gera o total de duração do dia e insere na lista de durações
                duracao_atual = gera_total_duracao(lista_tarefas_aux)
                self.total_duracao.insert(x, gera_total_duracao(lista_tarefas_aux))
                lista_tarefas_aux = [] # Limpa a lista de tarefas
                data_aux = data_aux + timedelta(days=1)  # Acrescenta um dia

        return lista_tarefas


def gera_total_duracao(lista_tarefas):
    """
    Recebe uma lista de tarefas e soma o total de duração
    """
    total_duracao = timedelta(days=0, hours=0, microseconds=0, milliseconds=0, minutes=0, weeks=0)
    if lista_tarefas is not None:
        for tarefa in lista_tarefas:
            if tarefa.duracao:
                total_duracao = total_duracao + tarefa.duracao
    return total_duracao





## ANTIGO PRODUTIVER ___

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
