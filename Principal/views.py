from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect

from Principal.models import Usuario,Nota,ReporteUsuario,ReporteNota,Seccion,MensajeDirecto,UsuarioSigueUsuario,Comentario,LikeNota
from rest_framework import viewsets
from Principal.serializers import UsuarioSerializer,NotaSerializer,ReporteUsuarioSerializer,ReporteNotaSerializer,SeccionSerializer

from Principal.forms import NuevaNotaForm, NuevoUsuarioForm, LoginForm

from django.template import RequestContext

from django.shortcuts import render_to_response, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.http import JsonResponse

from django.contrib.humanize.templatetags.humanize import naturaltime

#Viwesets para el API REST
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class ReporteUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ReporteUsuario.objects.all()
    serializer_class = ReporteUsuarioSerializer

class ReporteNotaViewSet(viewsets.ModelViewSet):
    queryset = ReporteNota.objects.all()
    serializer_class = ReporteNotaSerializer	

class SeccionViewSet(viewsets.ModelViewSet):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer	

#Listas
def lista_reportes(request):
	ctx = {'nombre_vista': 'Lista de Reportes de Notas'}
	return render(request, 'reportes.html', ctx)

def lista_reportes_usuario(request):
	ctx = {'nombre_vista': 'Lista de Reportes de Usuario'}
	return render(request, 'reportes_usuarios.html', ctx)

def lista_usuarios(request):
	ctx = {'nombre_vista': 'Lista de Usuarios'}
	return render(request, 'usuarios_admin.html', ctx)

def lista_mensajes(request):

	mensajes = MensajeDirecto.objects.filter( usuario_destinatario = request.user )

	ctx = {'nombre_vista': 'Lista de Mensajes Directos', 'mensajes': mensajes}

	return render(request, 'lista_mensajes.html', ctx)

def lista_seguidos(request, id):
	siguiendo = UsuarioSigueUsuario.objects.filter(usuario_seguidor = id)

	ctx = {'nombre_vista': 'Lista de Seguidos', 'siguiendo': siguiendo}
	return render(request, 'lista_siguiendo.html', ctx)

def lista_seguidores(request, id):
	seguidores = UsuarioSigueUsuario.objects.filter(usuario_seguido = id)


	ctx = {'nombre_vista': 'Lista de Seguidores', 'seguidores': seguidores}
	return render(request, 'lista_seguidores.html', ctx)

def lista_publicaciones(request):
	notas = Nota.objects.all()

	ctx = {'nombre_vista': 'Lista de Notas', 'notas': notas}
	return render(request, 'lista_publicaciones.html', ctx)

def lista_publicaciones_usuario(request, id):
	usuario = Usuario.objects.get(id = id)
	notas = Nota.objects.filter(usuario = usuario)

	ctx = {'nombre_vista': 'Lista de Notas', 'notas': notas}
	return render(request, 'lista_publicaciones.html', ctx)

def lista_publicaciones_seccion(request):
	ctx = {'nombre_vista': 'Lista de Publicaciones en Seccion'}
	return render(request, 'lista_publicaciones_seccion.html', ctx)	

def lista_subsecciones(request):
	ctx = {'nombre_vista': 'Lista de Subsecciones'}
	return render(request, 'lista_subsecciones.html', ctx)		

def lista_secciones(request):
	secciones = Seccion.objects.all()

	ctx = {'nombre_vista': 'Lista de Secciones', 'secciones': secciones}
	return render(request, 'lista_secciones.html', ctx)		

#Muestran info
def index(request):
	noticias = Nota.objects.all()

	ctx = {'noticias': noticias}
	return render(request, 'index.html', ctx)

def perfil(request, id):
	usuario = Usuario.objects.get(id = id)
	ctx = {'usuario': usuario}
	return render(request, 'perfil.html', ctx)

def publicacion(request, id):
	publicacion = Nota.objects.get(id = id)
	comentarios = Comentario.objects.filter(nota = publicacion)

	likes = LikeNota.objects.filter(nota = publicacion, usuario = request.user)
	like = False

	if likes.count() > 0:
		like = True

	ctx = {'publicacion': publicacion, 'comentarios': comentarios, 'like': like}
	return render(request, 'publicacion.html', ctx)


#Formularios
@login_required(login_url='/login')
def nuevo_post(request):
	p = True

	ctx = {}
	if request.method == 'POST':
		form = NuevaNotaForm(request.POST, request.FILES)
		if form.is_valid():
			titulo = form.cleaned_data['titulo']
			descripcion = form.cleaned_data['descripcion']
			subseccion = form.cleaned_data['subseccion']
			privacidad = form.cleaned_data['privacidad']
			imagen = request.FILES['imagen']

			if privacidad == 'publico':
				p = True
			else:
				p = False

			nota = Nota()
			nota.usuario = request.user
			nota.titulo = titulo
			nota.descripcion = descripcion
			nota.subseccion = subseccion
			nota.privacidad = p
			nota.imagen = imagen

			nota.longitud = 19.476286
			nota.latitud = -99.097218

			nota.save()

			return HttpResponseRedirect('/')
	else:
		form = NuevaNotaForm()

	ctx = {'form':form}
	return render(request,'nuevo_post.html',ctx)

def nuevo_usuario(request):
	ctx = {}
	if request.method == 'POST':
		form = NuevoUsuarioForm(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data['username']
			nombre = form.cleaned_data['nombre']
			ap_paterno = form.cleaned_data['ap_paterno']
			ap_materno = form.cleaned_data['ap_materno']
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			imagen = request.FILES['imagen']

			u = Usuario.objects.create_user(username, password)

			u.nombre = nombre
			u.ap_paterno = ap_paterno
			u.ap_materno = ap_materno
			u.username = username
			u.correo = email

			u.foto = imagen

			u.save()

			access = authenticate(username=username, password=password)
			if access is not None:
				if access.is_active:
					login(request,access)
					return HttpResponseRedirect('/')
				else:
					return render_to_response('noactive.html', context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/')
	else:
		form = NuevoUsuarioForm()

	ctx = {'form':form}
	return render(request,'nuevo_usuario.html',ctx)

@login_required(login_url='/login')
def editar_perfil(request, id):
	ctx = {}

	u = Usuario.objects.get(id = id)

	if request.method == 'GET':
		form = NuevoUsuarioForm(initial={
					'username': u.username,
					'nombre': u.nombre,
					'ap_paterno': u.ap_paterno,
					'ap_materno': u.ap_materno,
					'email': u.correo,
					'imagen': u.foto,
				})

	if request.method == 'POST':
		form = NuevoUsuarioForm(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data['username']
			nombre = form.cleaned_data['nombre']
			ap_paterno = form.cleaned_data['ap_paterno']
			ap_materno = form.cleaned_data['ap_materno']
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			imagen = request.FILES['imagen']

			u.nombre = nombre
			u.ap_paterno = ap_paterno
			u.ap_materno = ap_materno
			u.username = username
			u.correo = email

			u.foto = imagen

			u.save()

			access = authenticate(username=username, password=password)
			if access is not None:
				if access.is_active:
					login(request,access)
					return HttpResponseRedirect('/')
				else:
					return render_to_response('noactive.html', context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/')


	ctx = {'form':form}
	return render(request,'nuevo_usuario.html',ctx)




@login_required(login_url='/login')
def editar_post(request, id):
	p = True
	ctx = {}

	nota = Nota.objects.get(id = id)

	if request.method == 'GET':
		if nota.privacidad == True:
			privacidad = 'publico'
		else:
			privacidad = 'privado'

		form = NuevaNotaForm(initial={
					'titulo':nota.titulo,
					'descripcion':nota.descripcion,
					'imagen':nota.imagen,
					'subseccion':nota.subseccion,
					'privacidad':privacidad
				})

	if request.method == 'POST':
		form = NuevaNotaForm(request.POST, request.FILES)
		if form.is_valid():
			titulo = form.cleaned_data['titulo']
			descripcion = form.cleaned_data['descripcion']
			subseccion = form.cleaned_data['subseccion']
			privacidad = form.cleaned_data['privacidad']
			imagen = request.FILES['imagen']

			if privacidad == 'publico':
				p = True
			else:
				p = False

			nota.usuario = request.user
			nota.titulo = titulo
			nota.descripcion = descripcion
			nota.subseccion = subseccion
			nota.privacidad = p
			nota.imagen = imagen

			nota.longitud = 19.476286
			nota.latitud = -99.097218

			nota.save()

			return HttpResponseRedirect('/')

	ctx = {'form':form}

	return render(request, 'editar_post.html', ctx)

#Sesiones
def login_usuario(request):
	ctx = {}
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid:
			username = request.POST['username']
			password = request.POST['password']

			access = authenticate(username=username, password=password)
			if access is not None:
				if access.is_active:
					login(request,access)
					return HttpResponseRedirect('/')
				else:
					return render(request, 'noactive.html', ctx)
			else:
				return HttpResponseRedirect('/login')
	else:
		form = LoginForm()

	ctx = {'form':form}
	return render(request,'login.html',ctx)

def logout_usuario(request):
	logout(request)
	return HttpResponseRedirect('/login/')


#Ajax
def get_chat(request):
	usuario = request.GET.get('usuario_consultor', None)
	usuario_chat = request.GET.get('usuario_chat', None)

	mensajes = list(MensajeDirecto.objects.filter(Q(usuario_remitente = usuario, usuario_destinatario = usuario_chat) | Q(usuario_remitente = usuario_chat, usuario_destinatario = usuario)).values())


	for mensaje in mensajes:
		mensaje['fecha'] = naturaltime(mensaje['fecha']);

	return JsonResponse(mensajes, safe=False)


def get_puntos(request):

	notas = list(Nota.objects.all().values())

	print notas

	return JsonResponse(notas, safe=False)


def nuevo_comentario(request):
	contenido = request.GET['comentario']
	id_post = request.GET['id_post']
	id_usuario = request.GET['id_usuario']


	usuario = Usuario.objects.get(id = id_usuario)
	nota = Nota.objects.get(id = id_post)

	comentario = Comentario()

	comentario.contenido = contenido
	comentario.usuario = usuario
	comentario.nota = nota

	comentario.save()

	comentario_json = {'contenido': comentario.contenido, 'usuario': usuario.username, 'imagen': str(usuario.foto)}

	return JsonResponse(comentario_json, safe=False)

def like(request):

	id_post = request.GET['id_post']
	id_usuario = request.GET['id_usuario']

	like = request.GET['like']
	usuario = Usuario.objects.get(id = id_usuario)
	nota = Nota.objects.get(id = id_post)

	if like == 'true':
		like = LikeNota.objects.get(usuario = usuario, nota = nota)
		like.delete()
	else:
		like = LikeNota()
		like.nota = nota
		like.usuario = usuario
		like.save()
		
	respuesta = {'usuario': usuario.username, 'titulo': nota.titulo}
	return JsonResponse(respuesta, safe=False)


#Seguir y Dejar de Seguir
def dejar_de_seguir(request, id):

	usuario_seguido = Usuario.objects.get(id = id)

	u = UsuarioSigueUsuario.objects.get(usuario_seguido = usuario_seguido, usuario_seguidor = request.user)

	u.delete()


	return HttpResponseRedirect('/lista/seguidos/' + str(request.user.id))

def seguir(request, id):

	usu = UsuarioSigueUsuario()
	usu.usuario_seguido = Usuario.objects.get(id = id)
	usu.usuario_seguidor = Usuario.objects.get(id = request.user.id)

	usu.save()

	return HttpResponseRedirect('/perfil/' + str(id))