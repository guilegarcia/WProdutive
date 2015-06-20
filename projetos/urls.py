__author__ = 'GuiLe Garcia'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^criar-projeto/$', views.criar_projeto, name='criar_projeto'),
    url(r'^$', views.projetos, name='projetos'),
    url(r'^excluir/(?P<id>\d+)/$', views.excluir_projeto, name='excluir_projeto'),
    url(r'^editar-projeto/$', views.editar_projeto, name='editar_projeto'),
    url(r'^projeto/(?P<id>\d+)/$', views.projeto, name='projeto'), # todo mudar para slug
]