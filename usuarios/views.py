# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from papeis.models import Papel
from projetos.models import Projeto
from usuarios.forms import UsuarioForm


def criar_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = User.objects.create_user(**form.cleaned_data)
            usuario.save()
            messages.success(request, 'Conta criada com sucesso.')
    else:
        form = UsuarioForm()
    return render(request, 'criar-usuario.html', {'form': form})


@login_required()
def editar_usuario(request):
    form = UsuarioForm(request.POST or None, instance=request.user)
    if form.is_valid():
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        messages.success(request, 'Perfil atualizado com sucesso')
    return render(request, 'editar-perfil.html', {'form': form})

def fazer_login(request):
    """
    :param request.GET['next']: envia a página aonde redirecionar depois do login (pega da url)
    :param request.POST['next']: envia a página aonde redirecionar depois do login (pega do input hidden)
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Seta os projetos e papeis na session
                request.session['projetos'] = Projeto.objects.filter(usuario=user)
                request.session['papeis'] = Papel.objects.filter(usuario=user)
                return redirect(request.POST['next'])
        else:
            messages.error(request, 'A senha ou login estão incorretos. Tente novamente!')
            return redirect('/login/')
    else:
        return render(request, 'login.html', {'next': request.GET['next']})
