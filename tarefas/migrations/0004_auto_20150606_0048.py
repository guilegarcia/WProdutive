# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0003_auto_20150605_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='duracao',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
