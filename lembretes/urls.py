__author__ = 'GuiLe Garcia'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^criar-lembrete/$', views.criar_lembrete, name='criar_lembrete'),
    url(r'^excluir/(?P<id>\d+)/$', views.excluir_lembrete, name='excluir_lembrete'),
]
