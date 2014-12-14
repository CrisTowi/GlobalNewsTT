from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
from Principal.views import UsuarioViewSet, NotaViewSet, ReporteUsuarioViewSet,ReporteNotaViewSet,SeccionViewSet
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'reportesusuario', ReporteUsuarioViewSet)
router.register(r'reportesnota', ReporteNotaViewSet)
router.register(r'secciones', SeccionViewSet)


urlpatterns = patterns('',

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'Principal.views.index', name='index'),

    url(r'login/$', 'Principal.views.login_usuario', name='login_usuario'),
    url(r'logout/$', 'Principal.views.logout_usuario', name='logout_usuario'),

    url(r'perfil/(?P<id>\d+)$', 'Principal.views.perfil', name='perfil'),
    url(r'publicacion/(?P<id>\d+)$', 'Principal.views.publicacion', name='publicacion'),

    url(r'lista/nota/$', 'Principal.views.lista_publicaciones', name='lista_publicaciones'),
    url(r'lista/nota/usuario/(?P<id>\d+)$', 'Principal.views.lista_publicaciones_usuario', name='lista_publicaciones_usuario'),

    url(r'lista/nota/seccion/$', 'Principal.views.lista_publicaciones_seccion', name='lista_publicaciones_seccion'),
    url(r'lista/reportes/nota$', 'Principal.views.lista_reportes', name='lista_reportes'),
    url(r'lista/reportes/usuario$', 'Principal.views.lista_reportes_usuario', name='lista_reportes_usuario'),
    url(r'lista/usuarios/$', 'Principal.views.lista_usuarios', name='lista_usuarios'),
    url(r'lista/mensajes/$', 'Principal.views.lista_mensajes', name='lista_mensajes'),

    url(r'lista/seguidos/(?P<id>\d+)$', 'Principal.views.lista_seguidos', name='lista_seguidos'),
    url(r'lista/seguidores/(?P<id>\d+)$', 'Principal.views.lista_seguidores', name='lista_seguidores'),
    
    url(r'lista/subsecciones/$', 'Principal.views.lista_subsecciones', name='lista_subsecciones'),
    url(r'lista/secciones/$', 'Principal.views.lista_secciones', name='lista_secciones'),

    url(r'nuevo/nota/$', 'Principal.views.nuevo_post', name='nuevo_post'),
    url(r'nuevo/usuario/$', 'Principal.views.nuevo_usuario', name='nuevo_usuario'),

    url(r'editar/nota/(?P<id>\d+)$', 'Principal.views.editar_post', name='editar_post'),
    url(r'editar/usuario/(?P<id>\d+)$', 'Principal.views.editar_perfil', name='editar_perfil'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),


    #Vistas en AJAX
    url(r'chat/$', 'Principal.views.get_chat', name='get_chat'),
    url(r'puntos/$', 'Principal.views.get_puntos', name='get_puntos'),

    url(r'nuevo/comentario/$', 'Principal.views.nuevo_comentario', name='nuevo_comentario'),
    url(r'like/$', 'Principal.views.like', name='like'),
    url(r'dislike/$', 'Principal.views.dislike', name='dislike'),


    #Seguir y dejar de Seguir
    url(r'dejar_de_seguir/(?P<id>\d+)$', 'Principal.views.dejar_de_seguir', name='dejar_de_seguir'),
    url(r'seguir/(?P<id>\d+)$', 'Principal.views.seguir', name='seguir'),

)
