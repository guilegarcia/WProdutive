from django.contrib.auth.models import User
from rest_framework import serializers

from projetos.models import Projeto
from usuarios.serializers import UserSerializer


class ProjetoSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    #usuario = serializers.Field(source='request.user', required=False)
    # usuario = UserSerializer(required=False)

    class Meta:
        model = Projeto
        fields = ('pk', 'nome', 'descricao', 'usuario')
