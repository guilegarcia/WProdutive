# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Cria Lembrete
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from lembretes.forms import FormLembrete
from lembretes.models import Lembrete
from lembretes.serializers import LembreteSerializer


class LembreteViewSet(viewsets.ModelViewSet):
    """
    Listar, editar, criar e deletar
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Lembrete.objects.all()
    serializer_class = LembreteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Retorna a lista de projetos do usuário logado e a data
        """
        user = self.request.user

        # Verifica se possui data ou gera a lista de todos os lembretes do usuário (para editar e remover)
        if self.request.query_params.get('data') is not None:
            data = self.request.query_params.get('data', None)
            return Lembrete.objects.filter(data=data, usuario=user)
        else:
            return Lembrete.objects.filter(usuario=user)


@login_required()
# todo criar lembrete com jquery form (já está na pasta static/
def criar_lembrete(request):
    if request.method == 'POST':
        form = FormLembrete(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lembrete adicionado com sucesso')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, request.POST['url'], {'abrir_modal_lembrete': 'in', 'form': form})
    else:
        form = FormLembrete
        return render(request, 'dia.html', {'form': form})


@login_required()
def excluir_lembrete(request, id=None):
    lembrete = get_object_or_404(Lembrete, usuario=request.user, id=id)
    lembrete.delete()
    messages.success(request, 'Lembrete excluído com sucesso!')
    return redirect(request.META.get('HTTP_REFERER'))


"""
class CriarLembrete(SuccessMessageMixin, CreateView):
    form_class = Form88ct
    template_name = 'cadastro-88ct.html'
    success_url = '.'  # /execucoes/cadastrar-88ct/
    success_message = "Cadastro realizado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(Criar88ct, self).get_context_data(**kwargs)
        context['lista_unidades'] = UnidadePagadora.objects.filter(ativado=True)
        context['lista_acoes'] = Acao.objects.filter(ano=datetime.now().year) # Busca açoes do ano atual
        context['ativa_menu_solicitar'] = 'active'
        # Verifica se a execução pendente já foi inserida no banco de dados
        try:
            context['execucao_pendente'] = StatusExecucao.objects.get(nome="Pendente")
        except ObjectDoesNotExist:
            pass
        return context

    def form_valid(self, form):
        execucao = form.save(commit=False)
        execucao.dimensao = execucao.acao.dimensao
        execucao.tipo = '88CT'
        execucao.save()
        # Adiciona a execução no contexto da página (para imprimir)
        context = self.get_context_data(form=form)
        context['execucao'] = execucao
        messages.success(self.request, 'Cadastro realizado! Por favor, imprima o formulário!')
        return self.render_to_response(context)

    def form_invalid(self, form):
        messages.error(self.request, "Preencha o formulário corretamente!")
"""
