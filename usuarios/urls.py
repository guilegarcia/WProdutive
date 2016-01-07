__author__ = 'GuiLe Garcia'
from django.conf.urls import url

from usuarios.views import UsuarioCreate, UsuarioUpdate

urlpatterns = [
    url(r'^criar/$', UsuarioCreate.as_view(), name='criar_usuario'),
    # url(r'^editar-perfil/$', views.editar_usuario, name='editar_perfil'),
    url(r'^editar/(?P<pk>\d+)/$', UsuarioUpdate.as_view(), name='editar_perfil', ),
]
