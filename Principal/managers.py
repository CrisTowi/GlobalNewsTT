#encoding:utf-8
from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Debes elegir un nombre')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.perfil = 'administrador'
        user.administrador = True
        user.is_superuser = True
        user.save(using=self._db)
        return user