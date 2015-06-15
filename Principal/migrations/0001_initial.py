# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.CharField(max_length=45)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LikeNota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='MensajeDirecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.CharField(max_length=50)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('leido', models.BooleanField(default=False)),
                ('chat', models.ForeignKey(related_name='chat', to='Principal.Chat')),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=45)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(null=True, upload_to=b'notas', blank=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('longitud', models.FloatField()),
                ('latitud', models.FloatField()),
                ('privacidad', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReporteNota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.TextField(default=b'')),
                ('tipo', models.CharField(max_length=45)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('nota', models.ForeignKey(related_name='nota_reportenota', to='Principal.Nota')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.TextField(default=b'')),
                ('tipo', models.CharField(max_length=45)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45)),
                ('imagen', models.ImageField(null=True, upload_to=b'secciones', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subseccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45)),
                ('seccion', models.ForeignKey(related_name='seccion_subseccion', to='Principal.Seccion')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioSigueSeccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seccion', models.ForeignKey(related_name='seccion_seguidausuario', to='Principal.Seccion')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioSigueUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=25, db_index=True)),
                ('nombre', models.CharField(max_length=45)),
                ('ap_paterno', models.CharField(max_length=45)),
                ('ap_materno', models.CharField(max_length=45)),
                ('correo', models.CharField(max_length=45)),
                ('foto', models.ImageField(null=True, upload_to=b'usuarios', blank=True)),
                ('estado', models.CharField(max_length=45)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('activo', models.BooleanField(default=True, help_text=b'Activa un usuario para poder usar el sistema')),
                ('administrador', models.BooleanField(default=False, help_text=b'Que usuarios se les permite entrar al administrador')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='usuariosigueusuario',
            name='usuario_seguido',
            field=models.ForeignKey(related_name='usuario_seguido', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usuariosigueusuario',
            name='usuario_seguidor',
            field=models.ForeignKey(related_name='usuario_seguidor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usuariosigueseccion',
            name='usuario',
            field=models.ForeignKey(related_name='usuario_sigueseccion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reporteusuario',
            name='usuario_reportado',
            field=models.ForeignKey(related_name='usuario_reportado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reporteusuario',
            name='usuario_reportador',
            field=models.ForeignKey(related_name='usuario_reportador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reportenota',
            name='usuario',
            field=models.ForeignKey(related_name='usuario_reportenota', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nota',
            name='subseccion',
            field=models.ForeignKey(related_name='subseccion_nota', to='Principal.Subseccion'),
        ),
        migrations.AddField(
            model_name='nota',
            name='usuario',
            field=models.ForeignKey(related_name='usuario_nota', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mensajedirecto',
            name='usuario_destinatario',
            field=models.ForeignKey(related_name='usuario_destinatario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mensajedirecto',
            name='usuario_remitente',
            field=models.ForeignKey(related_name='usuario_remitente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likenota',
            name='nota',
            field=models.ForeignKey(related_name='like_nota', to='Principal.Nota'),
        ),
        migrations.AddField(
            model_name='likenota',
            name='usuario',
            field=models.ForeignKey(related_name='usuario_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comentario',
            name='nota',
            field=models.ForeignKey(related_name='nota_comentario', to='Principal.Nota'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(related_name='usuario_comentario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='usuario_dos',
            field=models.ForeignKey(related_name='usuario_dos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='usuario_uno',
            field=models.ForeignKey(related_name='usuario_uno', to=settings.AUTH_USER_MODEL),
        ),
    ]
