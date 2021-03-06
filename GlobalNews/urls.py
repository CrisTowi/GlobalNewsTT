from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
import notifications
from Principal.views import UsuarioViewSet, NotaViewSet, ReporteUsuarioViewSet,ReporteNotaViewSet,SeccionViewSet,UsuarioSigueUsuarioViewSet,ComentarioViewSet,UsuarioSigueSeccionViewSet,SubseccionViewSet,ChatViewSet,MensajeDirectoViewSet
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'reportesusuario', ReporteUsuarioViewSet)
router.register(r'reportesnota', ReporteNotaViewSet)
router.register(r'secciones', SeccionViewSet)
router.register(r'subseccion', SubseccionViewSet)
router.register(r'usuario_sigue_usuario', UsuarioSigueUsuarioViewSet)
router.register(r'usuario_sigue_seccion', UsuarioSigueSeccionViewSet)
router.register(r'comentario', ComentarioViewSet)
router.register(r'chat', ChatViewSet)
router.register(r'mensaje_directo', MensajeDirectoViewSet)

urlpatterns = patterns('',
    url('^inbox/notifications/', include(notifications.urls)),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'Principal.views.index', name='index'),

    url(r'login/$', 'Principal.views.login_usuario', name='login_usuario'),
    url(r'logout/$', 'Principal.views.logout_usuario', name='logout_usuario'),

    url(r'perfil/(?P<id>\d+)$', 'Principal.views.perfil', name='perfil'),
    url(r'publicacion/(?P<id>\d+)$', 'Principal.views.publicacion', name='publicacion'),
    url(r'publicacion/geolocalizacion/(?P<id>\d+)$', 'Principal.views.publicacion_geolocalizacion', name='publicacion_geolocalizacion'),

    url(r'lista/nota/$', 'Principal.views.lista_publicaciones', name='lista_publicaciones'),
    url(r'lista/nota/usuario/(?P<id>\d+)$', 'Principal.views.lista_publicaciones_usuario', name='lista_publicaciones_usuario'),

    url(r'lista/nota/seccion/(?P<id>\d+)$', 'Principal.views.lista_publicaciones_seccion', name='lista_publicaciones_seccion'),
   
    url(r'lista/notificaciones$', 'Principal.views.lista_notificaciones', name='lista_notificaciones'),

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

    url(r'eliminar/nota/(?P<id>\d+)$', 'Principal.views.eliminar_post', name='eliminar_post'),

    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),


    url(r'busca/nota/$', 'Principal.views.encuentra_nota', name='encuentra_nota'),
    url(r'busca/reporte/nota/$', 'Principal.views.encuentra_reporte_nota', name='encuentra_reporte_nota'),
    url(r'busca/reporte/usuario/$', 'Principal.views.encuentra_reporte_usuario', name='encuentra_reporte_usuario'),

    #Vistas en AJAX
    url(r'secciones/usuario/(?P<id>\d+)$', 'Principal.views.lista_secciones_usuarios', name='lista_secciones_usuarios'),
    url(r'mensajes/chat/(?P<id>\d+)$', 'Principal.views.mensajes_chat', name='mensajes_chat'),

    url(r'chat/$', 'Principal.views.get_chat', name='get_chat'),
    url(r'puntos/$', 'Principal.views.get_puntos', name='get_puntos'),
    url(r'get/chat/(?P<id>\d+)$', 'Principal.views.get_chat_id', name='get_chat_id'),

    url(r'nuevo/comentario/$', 'Principal.views.nuevo_comentario', name='nuevo_comentario'),
    url(r'eliminar/comentario/(?P<id>\d+)$', 'Principal.views.eliminar_comentario', name='eliminar_comentario'),
    url(r'like/$', 'Principal.views.like', name='like'),

    url(r'nuevo/mensaje/$', 'Principal.views.nuevo_mensaje', name='nuevo_mensaje'),
    url(r'eliminar/mensaje/$', 'Principal.views.eliminar_mensaje', name='eliminar_mensaje'),
    url(r'lista/seguidores/ajax/(?P<id>\d+)$', 'Principal.views.lista_seguidores_ajax', name='lista_seguidores_ajax'),
    url(r'lista/seguidos/ajax/(?P<id>\d+)$', 'Principal.views.lista_seguidos_ajax', name='lista_seguidos_ajax'),

    url(r'lista/notas/usuario/ajax/(?P<username>\w+)/$', 'Principal.views.lista_notas_usuarios_ajax', name='lista_notas_usuarios_ajax'),

    url(r'lista/notas/seccion/ajax/(?P<id>\d+)$', 'Principal.views.lista_notas_seccion_ajax', name='lista_notas_seccion_ajax'),

    url(r'lista/novedades$', 'Principal.views.novedades', name='novedades'),
    url(r'lista/populares$', 'Principal.views.usuarios_populares', name='usuarios_populares'),

    url(r'chats/usuario/(?P<id>\d+)$', 'Principal.views.chats_usuario', name='chats_usuario'),

    #Seguir y dejar de Seguir
    url(r'unfollow/(?P<id>\d+)$', 'Principal.views.dejar_de_seguir', name='dejar_de_seguir'),
    url(r'seguir/(?P<id>\d+)$', 'Principal.views.seguir', name='seguir'),

    url(r'seguir/seccion/(?P<id>\d+)$', 'Principal.views.seguir_seccion', name='seguir_seccion'),
    url(r'unfollow/seccion/(?P<id>\d+)$', 'Principal.views.dejar_de_seguir_seccion', name='dejar_de_seguir_seccion'),
    
    #Notificaciones
    url(r'eliminar/notificacion/(?P<id>\d+)$', 'Principal.views.eliminar_notificacion', name='eliminar_notificacion'),
    url(r'leer/notificacion/(?P<id>\d+)$', 'Principal.views.leer_notificacion', name='leer_notificacion'),

    #Movil
    url(r'nuevo/post/$', 'Principal.views.nuevo_post_movil', name='nuevo_post_movil'),

    url(r'editar/nota/$', 'Principal.views.editar_nota_movil', name='editar_nota_movil'),
    url(r'editar/usuario/$', 'Principal.views.editar_usuario_movil', name='editar_usuario_movil'),

    url(r'nuevo_reporte_nota/$', 'Principal.views.nuevo_reporte_post', name='nuevo_reporte_post'),
    url(r'nuevo_reporte_usuario/$', 'Principal.views.nuevo_reporte_usuario', name='nuevo_reporte_usuario'),
    url(r'ver/usuario/(?P<username>\w+)/$', 'Principal.views.ver_usuario', name='ver_usuario'),

    url(r'cancelar/reporte/nota/(?P<id>\d+)$', 'Principal.views.cancelar_reporte_nota', name='cancelar_reporte_nota'),
    url(r'cancelar/reporte/usuario/(?P<id>\d+)$', 'Principal.views.cancelar_reporte_usuario', name='cancelar_reporte_usuario'),

    url(r'comentarios/nota/(?P<id>\d+)$', 'Principal.views.comentarios_noticias', name='comentarios_noticias'),
    url(r'like/movil/$', 'Principal.views.like_movil', name='like_movil'),

    url(r'unfollow/usuario/$', 'Principal.views.dejar_de_seguir_usuario_movil', name='dejar_de_seguir_usuario_movil'),
    url(r'unfollow/seccion/$', 'Principal.views.dejar_de_seguir_seccion_movil', name='dejar_de_seguir_seccion_movil'),


    #Administracion
    url(r'dardebaja/nota/(?P<id>\d+)$', 'Principal.views.dar_de_baja_nota', name='dar_de_baja_nota'),
    url(r'dardebaja/usuario/(?P<id>\d+)$', 'Principal.views.dar_de_baja_usuario', name='dar_de_baja_usuario'),

)
