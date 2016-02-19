from django.contrib.auth.models import User
from rest_framework import serializers

from papeis.models import Papel


class PapelSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Papel
        fields = ('pk', 'nome', 'descricao', 'usuario')
