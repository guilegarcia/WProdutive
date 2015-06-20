# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_auto_20150605_0209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lembrete',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Lembrete',
        ),
    ]
