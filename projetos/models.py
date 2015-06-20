from django.contrib.auth.models import User
from django.db import models

class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User)
    # slug = models.SlugField(max_length=100)