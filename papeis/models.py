from django.contrib.auth.models import User
from django.db import models

class Papel(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User)

    def __init__(self, *args, **kwargs):
        super(Papel, self).__init__(*args, **kwargs)