# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0006_reportenota_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporteusuario',
            name='descripcion',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
