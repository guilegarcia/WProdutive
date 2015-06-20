# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
        ('projetos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(default=0)),
                ('duracao', models.DurationField(null=True, blank=True)),
                ('prioridade', models.IntegerField(default=30, null=True, blank=True)),
                ('data', models.DateField()),
                ('hora', models.TimeField(null=True, blank=True)),
                ('papel', models.ForeignKey(blank=True, to='sistema.Papel', null=True)),
                ('projeto', models.ForeignKey(blank=True, to='projetos.Projeto', null=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
