from django.contrib.auth.models import User
from django.db import models

class Lembrete(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField()
    usuario = models.ForeignKey(User)

    def __init__(self, *args, **kwargs):
        super(Lembrete, self).__init__(*args, **kwargs)