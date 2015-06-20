# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0002_auto_20150605_0209'),
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='papel',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Papel',
        ),
    ]
