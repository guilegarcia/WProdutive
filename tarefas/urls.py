from tarefas.views import TarefaCreate

__author__ = 'GuiLe Garcia'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^criar/$', TarefaCreate.as_view(), name='criar_tarefa'),
    # url(r'^criar/$', views.criar_tarefa, name='criar_tarefa'),
    url(r'^buscar/$', views.buscar_tarefas, name='buscar_tarefas'),
    url(r'^editar/$', views.editar_tarefa, name='editar_tarefa'),
    url(r'^excluir/(?P<id>\d+)/$', views.excluir_tarefa, name='excluir_tarefa'),
    url(r'^alterar-status$', views.alterar_status, name='alterar_status_tarefa'),
]
