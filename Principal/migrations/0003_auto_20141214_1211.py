# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Principal', '0002_mensajedirecto_leido'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeNota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nota', models.ForeignKey(related_name=b'like_nota', to='Principal.Nota')),
                ('usuario', models.ForeignKey(related_name=b'usuario_like', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='nota',
            name='likes',
        ),
    ]
