from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect

from Principal.models import Usuario,Nota,ReporteUsuario,ReporteNota,Seccion
from rest_framework import viewsets
from Principal.serializers import UsuarioSerializer,NotaSerializer,ReporteUsuarioSerializer,ReporteNotaSerializer,SeccionSerializer

from Principal.forms import NuevaNotaForm, NuevoUsuarioForm, LoginForm

from django.template import RequestContext

from django.shortcuts import render_to_response, get_object_or_404

from django.contrib.auth.decorators import login_required

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
	ctx = {'nombre_vista': 'Lista de Mensajes Directos'}
	return render(request, 'lista_mensajes.html', ctx)

def lista_seguidos(request):
	ctx = {'nombre_vista': 'Lista de Seguidos'}
	return render(request, 'lista_seguidores.html', ctx)

def lista_seguidores(request):
	ctx = {'nombre_vista': 'Lista de Seguidores'}
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
	ctx = {'publicacion': publicacion}
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

			u.imagen = imagen

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

@login_required(login_url='/login')
def editar_perfil(request):
	ctx = {}
	return render(request, 'editar_perfil.html', ctx)

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