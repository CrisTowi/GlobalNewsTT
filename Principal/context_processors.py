from Principal.models import Seccion, Nota, UsuarioSigueUsuario, Chat, ReporteUsuario, ReporteNota, Usuario, LikeNota
from django.db.models import Q

from notifications.models import Notification
from datetime import datetime, timedelta

def secciones_processor(request):
	secciones = Seccion.objects.all()

	return {'secciones': secciones}


def seguidores_siguiendo_publicaciones_processor(request):
	usuario = request.user.id

	num_notas = Nota.objects.filter(usuario = usuario).count()
	num_siguiendo = UsuarioSigueUsuario.objects.filter(usuario_seguidor = usuario).count()
	num_seguidores = UsuarioSigueUsuario.objects.filter(usuario_seguido = usuario).count()

	return {'num_notas': num_notas, 'num_siguiendo': num_siguiendo, 'num_seguidores': num_seguidores}


def mensajes_directos_processor(request):
	chats = []
	if request.user.is_authenticated():
		chats = Chat.objects.filter(Q(usuario_uno = request.user) | Q(usuario_dos = request.user))
	return {'chats_processor': chats}

def notificaciones_processor(request):
	ctx = {}
	if request.user.is_authenticated():
		notificaciones= Notification.objects.filter(recipient = request.user).unread()[:5]
		ctx = {'notificaciones': notificaciones}
	return ctx 	

def novedades_processor(request):
	last_day = datetime.today() - timedelta(days=1)	
	novedades = Nota.objects.filter(fecha__gte = last_day).order_by('-fecha')
	lista_likes = []


	for publicacion in novedades:
		num_likes = LikeNota.objects.filter(nota = publicacion).count()
		lista_likes.append({'nota':publicacion,'num_likes': num_likes})

	novedades = sorted(lista_likes, key=lambda k: k['num_likes'], reverse=True)[:4]


	return {'novedades': novedades}

def usuarios_populares_processor(request):
	id_usuarios = []
	last_day = datetime.today() - timedelta(days=1)	
	novedades = Nota.objects.filter(fecha__gte = last_day).order_by('-fecha')
	lista_likes = []

	for publicacion in novedades:
		num_likes = LikeNota.objects.filter(nota = publicacion).count()
		lista_likes.append({'nota':publicacion,'num_likes': num_likes})

	novedades = sorted(lista_likes, key=lambda k: k['num_likes'], reverse=True)[:4]

	for novedad in novedades:
		id_usuarios.append(novedad['nota'].usuario.id)

	usuarios_populares = Usuario.objects.filter(id__in=id_usuarios)

	return {'usuarios_populares': usuarios_populares}	

def reportes(request):
	reportes_usuario = ReporteUsuario.objects.all().order_by('-id')[:2]
	reportes_nota = ReporteNota.objects.all().order_by('-id')[:2]

	return {'reportes_usuario_cp': reportes_usuario, 'reportes_nota_cp': reportes_nota}
