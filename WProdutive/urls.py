"""WProdutive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.auth.views import logout_then_login

from sistema import views as views_sistema
from usuarios import views as views_usuarios

urlpatterns = [
    # Teste angular
    url(r'^angular/$', views_sistema.teste_angular, name='teste_angular'),


    url(r'^$', views_sistema.index, name='index'),
    url(r'^dia/$', views_sistema.dia, name='dia'),
    url(r'^semana/$', views_sistema.semana, name='semana'),
    url(r'^tarefas/', include('tarefas.urls')),
    url(r'^projetos/', include('projetos.urls')),
    url(r'^papeis/', include('papeis.urls')),
    url(r'^lembretes/', include('lembretes.urls')),
    url(r'^usuarios/', include('usuarios.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    # Login autentificacao
    # url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^login/$', views_usuarios.fazer_login, name='login'),
    # url(r'^logout/$', logout_then_login, {'login_url': '/login/'}),
    url(r'^sair/$', logout_then_login, {'login_url': '/login/'}, name='logout'),
]
