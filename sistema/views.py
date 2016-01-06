# -*- encoding: utf-8 -*-
from datetime import timedelta, date
import locale
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lembretes.models import Lembrete
from sistema.forms import DiaForm, SemanaForm
from tarefas.models import Tarefa


# Dia
@login_required()
def dia(request):
    data = date.today()
    if request.method == 'POST':
        form = DiaForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            data = dados.get('data')
            # Dia Anterior
            if dados.get('ant_prox') == 'anterior':
                data_subtraida = data - timedelta(days=1)
                data = data_subtraida
            # Próximo dia
            elif dados.get('ant_prox') == 'proximo':
                # soma +1 na data
                data = data + timedelta(days=1)

    # Recebe tarefas, lembretes do dia
    lista_tarefas = list(Tarefa.objects.filter(data=data, usuario=request.user).order_by('prioridade'))
    lista_lembretes = Lembrete.objects.filter(data=data, usuario=request.user)

    # Tarefas atrasadas (exceto apartir de amanhã)
    if (data <= date.today()):
        lista_tarefas_atrasadas = list(Tarefa.objects.filter(usuario=request.user, status=0, data__lt=data))

        # Percorre a lista de atrasadas e seta 2 (atrasado) nas tarefas atrasadas
        if lista_tarefas_atrasadas:
            for x, tarefa in enumerate(lista_tarefas_atrasadas):
                lista_tarefas_atrasadas[x].status = 2

            # Concatena as duas listas
            lista_tarefas = lista_tarefas + lista_tarefas_atrasadas

    # Total Duração e Progresso
    total_duracao = gera_total_duracao(request, lista_tarefas)
    progresso = gera_progresso(request, lista_tarefas)

    return render(request, "dia.html",
                  {'lista_tarefas': lista_tarefas, 'lista_lembretes': lista_lembretes, 'dia_active': 'active',
                   'data': data, 'total_duracao': total_duracao, 'progresso': progresso})


@login_required()
def semana(request):
    data = date.today()
    if request.method == 'POST':
        form = SemanaForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            data = dados.get('data')
            # Subtrai 14 dias para semana anterior (próxima semana já está setado ao percorrer os 7 dias)
            if dados.get('ant_prox') == 'anterior':
                data = data - timedelta(days=7)
            else:
                data = data + timedelta(days=7)

    # Recebe a segunda-feira da semana a partir da data
    data = data - timedelta(days=data.weekday())

    # Insere dias da semana na session  (lembretes e tarefas)
    insere_dias_semana_session(request, data)

    return render(request, 'semana.html', {'data_semana': data})


@login_required()
def insere_dias_semana_session(request, data):
    """
    :param data: recebe a data do início da semana
    :param: datas_semana: recebe as datas da semana (para usar no template)
    data.strftime('tarefas_%a'): imprime "tarefas_qua"
    """
    # Seta a localização brasil (para imprimir o dia em pt-br)
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Testar em produção

    # Seta os dias da semana na session (de 0 (segunda) a domingo (7))
    data = data - timedelta(days=1)  # Inicia na segunda
    datas_semana = []
    for x in range(0, 6):
        data = data + timedelta(days=1)
        lista_tarefas = Tarefa.objects.filter(usuario=request.user, data=data)
        # Insere lista de tarefas e lembretes
        request.session[data.strftime('tarefas_%a')] = lista_tarefas
        request.session[data.strftime('lembretes_%a')] = Lembrete.objects.filter(usuario=request.user, data=data)
        # Datas da semana (usado no template)
        datas_semana.append(data)
        # Gera total duração
        total_duracao = gera_total_duracao(request, lista_tarefas)
        teste = data.strftime('total_horas_%a')  # Está imprimindo 'total_horas_s�b'
        request.session[data.strftime('total_horas_%a')] = total_duracao  # duracao_seg, ter, etc

    request.session['datas_semana'] = datas_semana


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
