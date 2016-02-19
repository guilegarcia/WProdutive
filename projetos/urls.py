__author__ = 'GuiLe Garcia'
from projetos.views import ProjetoList
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'^', views.ProjetoList)

urlpatterns = [
    # REST
    url(r'^api', include(router.urls)),

    url(r'^criar-projeto/$', views.criar_projeto, name='criar_projeto'),
    url(r'^$', views.projetos, name='projetos'),
    url(r'^excluir/(?P<id>\d+)/$', views.excluir_projeto, ),
    url(r'^editar/$', views.editar_projeto, name='editar_projeto'),
    url(r'^projeto/(?P<id>\d+)/$', views.projeto, name='projeto'), # todo mudar para slug

    # # REST
    #
    # url(r'^api/', ProjetoList.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # }), name='projeto_api'),
    #
    # url(r'^(?P<pk>[0-9]+)/api/$', ProjetoList.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # }), name='projeto_api_id'),
]
