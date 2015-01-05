# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0004_auto_20141227_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subseccion',
            name='tiempo_aparicion',
        ),
        migrations.RemoveField(
            model_name='usuariosigueseccion',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='usuariosigueusuario',
            name='fecha',
        ),
    ]
