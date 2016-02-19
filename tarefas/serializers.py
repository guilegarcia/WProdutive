from django.contrib.auth.models import User
from rest_framework import serializers

from papeis.models import Papel
from projetos.models import Projeto
from tarefas.models import Tarefa


class TarefaSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    papel = serializers.PrimaryKeyRelatedField(queryset=Papel.objects.all(), required=False, allow_null=True)
    projeto = serializers.PrimaryKeyRelatedField(queryset=Projeto.objects.all(), required=False, allow_null=True)
    tarefa_original = serializers.PrimaryKeyRelatedField(queryset=Tarefa.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Tarefa

        fields = (
            'pk', 'titulo', 'descricao', 'data', 'hora', 'duracao', 'prioridade', 'status', 'papel', 'projeto',
            'usuario', 'repetida', 'tarefa_original')
