from django.contrib.auth.models import User
from rest_framework import serializers

from lembretes.models import Lembrete


class LembreteSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Lembrete

        fields = ('pk', 'titulo', 'descricao', 'data', 'usuario')
