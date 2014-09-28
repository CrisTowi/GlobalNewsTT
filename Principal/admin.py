#encoding:utf-8

from django.contrib import admin
from Principal.models import Usuario, Comentario, ReporteNota, Nota, UsuarioSigueSeccion, UsuarioSigueUsuario, Subseccion, Seccion, ReporteUsuario, MensajeDirecto

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from forms import *


class MyUserAdmin(UserAdmin):
    form = CambiarusuarioForm
    add_form = CrearUsuarioForm

    list_display = ('username',)
    list_filter = ('username',)
    fieldsets = (
                (None, {'fields': ('username', 'password')}),
                ('Perfil', {'fields': ('nombre','foto','ap_paterno','ap_materno','correo','estado')}),
                ('Permisos', {'fields': ('administrador', 'activo', 'is_superuser', 'user_permissions')}),
    )
    add_fieldsets = (
                    (None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2',)}),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'user_permissions':
            query = Permission.objects.filter(content_type__app_label="Principal")
            kwargs['queryset'] = query
        return super(MyUserAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)


admin.site.register(Usuario, MyUserAdmin)
admin.site.register(Comentario)
admin.site.register(ReporteNota)
admin.site.register(Nota)
admin.site.register(UsuarioSigueSeccion)
admin.site.register(UsuarioSigueUsuario)
admin.site.register(Subseccion)
admin.site.register(Seccion)
admin.site.register(ReporteUsuario)
admin.site.register(MensajeDirecto)