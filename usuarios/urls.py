__author__ = 'GuiLe Garcia'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^criar-usuario/$', views.criar_usuario, name='criar_usuario'),
    url(r'^editar-perfil/$', views.editar_usuario, name='editar_perfil'),
]