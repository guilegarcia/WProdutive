# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0004_auto_20150606_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarefa',
            name='duracao',
            field=models.DurationField(null=True, blank=True),
        ),
    ]
