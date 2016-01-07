from django.contrib.auth.models import User
from django.db import models

from papeis.models import Papel
from projetos.models import Projeto


class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    duracao = models.DurationField(blank=True, null=True)
    prioridade = models.IntegerField(default=30, blank=True, null=True)
    status = models.IntegerField(default=0)
    papel = models.ForeignKey(Papel, blank=True, null=True)
    projeto = models.ForeignKey(Projeto, blank=True, null=True)
    usuario = models.ForeignKey(User)

    def __init__(self, *args, **kwargs):
        super(Tarefa, self).__init__(*args, **kwargs)
