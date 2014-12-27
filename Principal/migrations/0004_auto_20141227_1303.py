# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0003_auto_20141214_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario_dos', models.ForeignKey(related_name=b'usuario_dos', to=settings.AUTH_USER_MODEL)),
                ('usuario_uno', models.ForeignKey(related_name=b'usuario_uno', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mensajedirecto',
            name='chat',
            field=models.ForeignKey(related_name=b'chat', default=0, to='Principal.Chat'),
            preserve_default=False,
        ),
    ]
