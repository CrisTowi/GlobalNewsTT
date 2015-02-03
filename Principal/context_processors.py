from Principal.models import Seccion, Nota, UsuarioSigueUsuario, Chat, ReporteUsuario, ReporteNota
from django.db.models import Q


def secciones_processor(request):
	secciones = Seccion.objects.all()

	return {'secciones': secciones}


def seguidores_siguiendo_publicaciones_processor(request):
	usuario = request.user.id

	num_notas = Nota.objects.filter(usuario = usuario).count()
	num_siguiendo = UsuarioSigueUsuario.objects.filter(usuario_seguidor = usuario).count()
	num_seguidores = UsuarioSigueUsuario.objects.filter(usuario_seguido = usuario).count()

	return {'num_notas': num_notas, 'num_siguiendo': num_siguiendo, 'num_seguidores': num_seguidores}

def novedades_processor(request):
	novedades = Nota.objects.all().order_by('-fecha')[:4]

	return {'novedades': novedades}

def mensajes_directos_processor(request):

	chats = []

	if request.user.is_authenticated():

		chats = Chat.objects.filter(Q(usuario_uno = request.user) | Q(usuario_dos = request.user))


	return {'chats_processor': chats}

def reportes(request):

	reportes_usuario = ReporteUsuario.objects.all()[:2]
	reportes_nota = ReporteNota.objects.all()[:2]

	print reportes_nota

	return {'reportes_usuario': reportes_usuario, 'reportes_nota': reportes_nota}
