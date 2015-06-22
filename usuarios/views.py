# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from papeis.models import Papel
from projetos.models import Projeto
from usuarios.forms import UsuarioForm


# Define que precisa de login
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class UsuarioCreate(SuccessMessageMixin, CreateView):
    model = User
    fields = ['first_name', 'username', 'email', 'password']
    template_name = 'criar-usuario.html'
    success_url = '/usuarios/criar/'
    success_message = "Usuário criado com sucesso"

class UsuarioUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'email', 'password']
    template_name = 'editar-perfil.html'
    success_message = 'Usuário atualizado com sucesso!'

    # success_url = '/usuarios/editar-perfil/'

    def get_success_url(self, **kwargs):
        return reverse_lazy('editar_perfil', kwargs = {'pk': self.kwargs['pk']})


"""
@login_required()
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
"""

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
        return render(request, 'login.html', {'next': request.GET.get('next')})
