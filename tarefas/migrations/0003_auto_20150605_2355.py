# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0002_auto_20150605_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='duracao',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
