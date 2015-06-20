# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Cria Lembrete
from lembretes.forms import FormLembrete
from lembretes.models import Lembrete


@login_required()
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
    lembrete = get_object_or_404(Lembrete, usuario = request.user, id=id)
    lembrete.delete()
    messages.success(request, 'Lembrete excluído com sucesso!')
    return redirect(request.META.get('HTTP_REFERER'))

