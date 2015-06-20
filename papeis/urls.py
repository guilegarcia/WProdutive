__author__ = 'GuiLe Garcia'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^criar-papel/$', views.criar_papel, name='criar_papel'),
    url(r'^$', views.papeis, name='papeis'),
    url(r'^excluir/(?P<id>\d+)/$', views.excluir_papel, name='excluir_papel'),
    url(r'^editar/$', views.editar_papel, name='editar_papel'),
    url(r'^papel/(?P<id>\d+)/$', views.papel, name='papel') # todo mudar para slug
]