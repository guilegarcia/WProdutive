from rest_framework.routers import DefaultRouter

__author__ = 'GuiLe Garcia'
from django.conf.urls import url, include

from . import views

# Create a router and register our viewsets with it. # REST
router = DefaultRouter()
router.register(r'^', views.PapelViewSet)

urlpatterns = [
    url(r'^criar-papel/$', views.criar_papel, name='criar_papel'),
    url(r'^$', views.papeis, name='papeis'),
    url(r'^excluir/(?P<id>\d+)/$', views.excluir_papel, name='excluir_papel'),
    url(r'^editar/$', views.editar_papel, name='editar_papel'),
    url(r'^papel/(?P<id>\d+)/$', views.papel, name='papel'),  # todo mudar para slug

    # REST
    url(r'^api', include(router.urls)),
]
