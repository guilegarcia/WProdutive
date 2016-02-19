from rest_framework.routers import DefaultRouter

__author__ = 'GuiLe Garcia'
from django.conf.urls import url, include

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'^', views.LembreteViewSet)

urlpatterns = [
    url(r'^criar-lembrete/$', views.criar_lembrete, name='criar_lembrete'),
    url(r'^excluir/(?P<id>\d+)/$', views.excluir_lembrete, name='excluir_lembrete'),

    # REST
    url(r'^api', include(router.urls)),
]
