from django.shortcuts import render, render_to_response
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect

from Principal.models import Chat,Usuario,Nota,ReporteUsuario,ReporteNota,Seccion,MensajeDirecto,UsuarioSigueUsuario,Comentario,LikeNota,Subseccion, UsuarioSigueSeccion

from notifications.models import Notification

from rest_framework import viewsets
from Principal.serializers import UsuarioSerializer,NotaSerializer,ReporteUsuarioSerializer,ReporteNotaSerializer,SeccionSerializer,UsuarioSigueUsuarioSerializer,ComentarioSerializer, UsuarioSigueSeccionSerializer, SubseccionSerializer, ChatSerializer, MensajeDirectoSerializer

from Principal.forms import NuevaNotaForm, NuevoUsuarioForm, LoginForm, EditarUsuarioForm, ReporteNotaForm, ReporteUsuarioForm

from django.template import RequestContext

from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.http import JsonResponse

from django.contrib.humanize.templatetags.humanize import naturaltime

from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

import redis

from notifications import notify

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import Principal.helper as helper

from django.db.models import Count

#Cambiar host
HOST = "10.10.1.152"
#HOST = "localhost"

MAX_REPORTES = 5
CADUCA_REPORTES = 1

def session_from_usuario(id_usuario):
	sesiones = Session.objects.all()
	for sesion in sesiones:
		user_id = sesion.get_decoded().get('_auth_user_id')
		if str(user_id) == str(id_usuario):
			return sesion.session_key

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

class UsuarioSigueUsuarioViewSet(viewsets.ModelViewSet):
	queryset = UsuarioSigueUsuario.objects.all()
	serializer_class = UsuarioSigueUsuarioSerializer

class UsuarioSigueSeccionViewSet(viewsets.ModelViewSet):
	queryset = UsuarioSigueSeccion.objects.all()
	serializer_class = UsuarioSigueSeccionSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
	queryset = Comentario.objects.all()
	serializer_class = ComentarioSerializer

class SubseccionViewSet(viewsets.ModelViewSet):
	queryset = Subseccion.objects.all()
	serializer_class = SubseccionSerializer

class ChatViewSet(viewsets.ModelViewSet):
	queryset = Chat.objects.all()
	serializer_class = ChatSerializer

class MensajeDirectoViewSet(viewsets.ModelViewSet):
	queryset = MensajeDirecto.objects.all()
	serializer_class = MensajeDirectoSerializer

#Listas
@login_required(login_url='/login')
def lista_reportes(request):
	reportes = ReporteNota.objects.all().annotate(num_reportes=Count('id')).filter(num_reportes__gte=MAX_REPORTES)
	last_date = datetime.today() - timedelta(weeks=CADUCA_REPORTES)

	paginator = Paginator(reportes, 8)
 	page = request.GET.get('page')
 	try:
		reportes_nota = paginator.page(page)
 	except PageNotAnInteger:
		reportes_nota = paginator.page(1)
	except EmptyPage:
		reportes_nota = paginator.page(paginator.num_pages)

	reportes_pasados = ReporteNota.objects.all().annotate(num_reportes=Count('id')).filter(num_reportes__gte=MAX_REPORTES).filter(fecha__lte = last_date)

	ctx = {'reportes_nota': reportes_nota, 'nombre_vista': 'Lista de Reportes de Notas', 'reportes_pasados': reportes_pasados}
	return render(request, 'reportes.html', ctx)

@login_required(login_url='/login')
def lista_reportes_usuario(request):
	reportes = list(ReporteUsuario.objects.all().annotate(num_reportes=Count('id')).filter(num_reportes__gte=MAX_REPORTES))
	last_date = datetime.today() - timedelta(weeks=CADUCA_REPORTES)


	paginator = Paginator(reportes, 8)
 	page = request.GET.get('page')
 	try:
		reportes_usuario = paginator.page(page)
 	except PageNotAnInteger:
		reportes_usuario = paginator.page(1)
	except EmptyPage:
		reportes_usuario = paginator.page(paginator.num_pages)

	reportes_pasados = ReporteUsuario.objects.filter(fecha__lte = last_date)

	ctx = {'reportes_usuario': reportes_usuario, 'nombre_vista': 'Lista de Reportes de Usuario', 'reportes_pasados': reportes_pasados}
	return render(request, 'reportes_usuarios.html', ctx)

def lista_usuarios(request):
	ctx = {'nombre_vista': 'Lista de Usuarios'}
	return render(request, 'usuarios_admin.html', ctx)

@login_required(login_url='/login')
def lista_mensajes(request):
	chats = Chat.objects.filter(Q(usuario_uno = request.user) | Q(usuario_dos = request.user))

	ctx = {'nombre_vista': 'Lista de Mensajes Directos', 'chats': chats}

	return render(request, 'lista_mensajes.html', ctx)

@login_required(login_url='/login')
def lista_seguidos(request, id):
	lista_siguiendo = UsuarioSigueUsuario.objects.filter(usuario_seguidor = id)

	paginator = Paginator(lista_siguiendo, 9)
 	page = request.GET.get('page')
 	try:
		siguiendo = paginator.page(page)
 	except PageNotAnInteger:
		siguiendo = paginator.page(1)
	except EmptyPage:
		siguiendo = paginator.page(paginator.num_pages)

	ctx = {'nombre_vista': 'Lista de Seguidos', 'siguiendo': siguiendo}
	return render(request, 'lista_siguiendo.html', ctx)

@login_required(login_url='/login')
def lista_seguidores(request, id):
	lista_seguidores = UsuarioSigueUsuario.objects.filter(usuario_seguido = id)

	paginator = Paginator(lista_seguidores, 9)
 	page = request.GET.get('page')
 	try:
		seguidores = paginator.page(page)
 	except PageNotAnInteger:
		seguidores = paginator.page(1)
	except EmptyPage:
		seguidores = paginator.page(paginator.num_pages)

	ctx = {'nombre_vista': 'Lista de Seguidores', 'seguidores': seguidores}
	return render(request, 'lista_seguidores.html', ctx)

def lista_publicaciones(request):
	notas = Nota.objects.all()

	ctx = {'nombre_vista': 'Lista de Noticias', 'notas': notas}
	return render(request, 'lista_publicaciones.html', ctx)

def lista_publicaciones_usuario(request, id):
	usuario = Usuario.objects.get(id = id)
	lista_notas = Nota.objects.filter(usuario = usuario).order_by('-fecha')

	paginator = Paginator(lista_notas, 4)
 	page = request.GET.get('page')
 	try:
		notas = paginator.page(page)
 	except PageNotAnInteger:
		notas = paginator.page(1)
	except EmptyPage:
		notas = paginator.page(paginator.num_pages)

	ctx = {'nombre_vista': 'Lista de Noticias', 'notas': notas}
	return render(request, 'lista_publicaciones.html', ctx)

def lista_publicaciones_seccion(request, id):
	seccion = Seccion.objects.get(id = id)
	subseccion = Subseccion.objects.filter(seccion = seccion)

	if request.user.is_authenticated():
		usu = UsuarioSigueSeccion.objects.filter(seccion = seccion, usuario = request.user)
		if usu:
			follow = True
		else:
			follow = False
	else:
		follow = False

	lista_notas = Nota.objects.filter(subseccion = subseccion).order_by('-fecha')

	paginator = Paginator(lista_notas, 4)
 	page = request.GET.get('page')
 	try:
		notas = paginator.page(page)
 	except PageNotAnInteger:
		notas = paginator.page(1)
	except EmptyPage:
		notas = paginator.page(paginator.num_pages)

	ctx = {'nombre_vista': 'Lista de Publicaciones en ' + seccion.nombre , 'notas': notas, 'seccion': seccion, 'follow': follow}
	return render(request, 'lista_publicaciones_seccion.html', ctx)	

def lista_subsecciones(request):
	ctx = {'nombre_vista': 'Lista de Subsecciones'}
	return render(request, 'lista_subsecciones.html', ctx)		

def lista_secciones(request):
	secciones = Seccion.objects.all()

	ctx = {'nombre_vista': 'Lista de Secciones', 'secciones': secciones}
	return render(request, 'lista_secciones.html', ctx)		

@login_required(login_url='/login')
def lista_notificaciones(request):

	notificaciones= Notification.objects.filter(recipient = request.user)
	paginator = Paginator(notificaciones, 10)
 	page = request.GET.get('page')
 	try:
		lista_notificaciones = paginator.page(page)
 	except PageNotAnInteger:
		lista_notificaciones = paginator.page(1)
	except EmptyPage:
		lista_notificaciones = paginator.page(paginator.num_pages)


	ctx = {'nombre_vista': 'Lista de Notificaciones', 'lista_notificaciones': lista_notificaciones}

	return render(request, 'lista_notificaciones.html', ctx)

#Muestran info
def index(request):
	mensaje = ''
	page = ''
	last_day = datetime.today() - timedelta(days=1)
	if request.user.is_authenticated():
		siguiendo_seccion_id = UsuarioSigueSeccion.objects.filter(usuario = request.user).values_list('seccion', flat=True)
		subsecciones_id = Subseccion.objects.filter(seccion = siguiendo_seccion_id).values_list('id', flat=True)
		siguiendo_id = UsuarioSigueUsuario.objects.filter(usuario_seguidor = request.user).values_list('usuario_seguido', flat=True)
		lista_noticias = Nota.objects.filter((Q(usuario = siguiendo_id) | Q(usuario = request.user) | Q(subseccion = subsecciones_id)), fecha__gte=last_day).order_by('-fecha')
	else:
		lista_noticias = Nota.objects.filter(fecha__gte = last_day).order_by('-fecha')

	lista_noticias = list(lista_noticias.values())

	for noticia in lista_noticias:
		usuario = Usuario.objects.get(id = noticia['usuario_id'])
		noticia['usuario'] = {
			'username': usuario.username,
			'id': usuario.id
		}
		noticia['seccion_id'] = Subseccion.objects.get(id = noticia['subseccion_id']).seccion.id

	paginator = Paginator(lista_noticias, 6)
	if request.GET:
		mensaje = request.GET['mensaje']
 		page = request.GET.get('page')
 	try:
		noticias = paginator.page(page)
 	except PageNotAnInteger:
		noticias = paginator.page(1)
	except EmptyPage:
		noticias = paginator.page(paginator.num_pages)

	ctx = {'noticias': noticias, 'mensaje': mensaje}
	return render(request, 'index.html', ctx)

def perfil(request, id):
	form = ReporteUsuarioForm()

	perfil = Usuario.objects.get(id = id)
	num_siguiendo = UsuarioSigueUsuario.objects.filter(usuario_seguidor = perfil).count()
	num_seguidores = UsuarioSigueUsuario.objects.filter(usuario_seguido = perfil).count()

	if request.user.is_authenticated():
		usu = UsuarioSigueUsuario.objects.filter(usuario_seguido = perfil, usuario_seguidor = request.user)
		if usu:
			follow = True
		else:
			follow = False

	else:
		follow = False

	ctx = {'perfil': perfil, 'follow': follow, 'form': form, 'numero_siguiendo': num_siguiendo, 'numero_seguidores': num_seguidores}
	return render(request, 'perfil.html', ctx)

def publicacion(request, id):
	form = ReporteNotaForm()
	publicacion = Nota.objects.get(id = id)
	comentarios = Comentario.objects.filter(nota = publicacion).order_by('-fecha')
	like = False
	num_likes = LikeNota.objects.filter(nota = publicacion).count()

	if publicacion.privacidad == False:
		if request.user.is_authenticated():
			likes = LikeNota.objects.filter(nota = publicacion, usuario = request.user)
			if likes.count() > 0:
				like = True

			ctx = {'publicacion': publicacion, 'comentarios': comentarios, 'like': like, 'num_likes': num_likes, 'form': form}
			return render(request, 'publicacion.html', ctx)

		else:
			return render(request, '404.html', {})

	else:
		if request.user.is_authenticated():
			likes = LikeNota.objects.filter(nota = publicacion, usuario = request.user)
			if likes.count() > 0:
				like = True

			ctx = {'publicacion': publicacion, 'comentarios': comentarios, 'like': like, 'num_likes': num_likes, 'form': form}
			return render(request, 'publicacion.html', ctx)
		else:
			ctx = {'publicacion': publicacion, 'comentarios': comentarios, 'like': like, 'num_likes': num_likes, 'form': form}
			return render(request, 'publicacion.html', ctx)

def publicacion_geolocalizacion(request, id):
	form = ReporteNotaForm()
	publicacion = Nota.objects.get(id = id)
	comentarios = Comentario.objects.filter(nota = publicacion).order_by('-fecha')
	like = False
	num_likes = LikeNota.objects.filter(nota = publicacion).count()

	if publicacion.privacidad == False:
		if request.user.is_authenticated():
			likes = LikeNota.objects.filter(nota = publicacion, usuario = request.user)
			if likes.count() > 0:
				like = True

			ctx = {'publicacion': publicacion, 'comentarios': comentarios, 'like': like, 'num_likes': num_likes, 'form': form}
			return render(request, 'publicacion_geolocalizacion.html', ctx)
		else:
			return render(request, '404.html', {})

	else:
		if request.user.is_authenticated():
			likes = LikeNota.objects.filter(nota = publicacion, usuario = request.user)
			if likes.count() > 0:
				like = True

			ctx = {'publicacion': publicacion, 'comentarios': comentarios, 'like': like, 'num_likes': num_likes, 'form': form}
			return render(request, 'publicacion_geolocalizacion.html', ctx)
		else:
			ctx = {'publicacion': publicacion, 'comentarios': comentarios, 'like': like, 'num_likes': num_likes, 'form': form}
			return render(request, 'publicacion_geolocalizacion.html', ctx)


#Formularios
@login_required(login_url='/login')
def nuevo_reporte_post(request):
	usuario = request.user
	nota = Nota.objects.get(id = int(request.POST['publicacion_id']))
	tipo = request.POST['razon']
	descripcion = request.POST['descripcion']

	reporte_nota = ReporteNota()
	reporte_nota.usuario = usuario
	reporte_nota.nota = nota
	reporte_nota.tipo = tipo
	reporte_nota.descripcion = descripcion

	reporte_nota.save()
	num_reportes = ReporteNota.objects.filter(nota = nota).count()
	key_sesion = session_from_usuario(nota.usuario.id)

	if (num_reportes >= MAX_REPORTES):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		r.publish('nota_reportada', '{"session_key": "' + str(key_sesion) + '", "nota_id": "' +str(nota.id)+ '", "nota": "'+ nota.titulo +'" }')

		notify.send(
	            reporte_nota,
	            description= str(nota) + ' ha sido reportada mas de '+str(MAX_REPORTES)+' veces ',
	            recipient=nota.usuario,
	            target=nota,
	            verb= 'nota_reportada'
	        )

	return HttpResponseRedirect('/?mensaje=Reporte%20creado%20correctamente')


@login_required(login_url='/login')
def cancelar_reporte_nota(request, id):
	reporte_nota = ReporteNota.objects.get(id=id)
	reporte_nota.delete()
	return HttpResponseRedirect('/lista/reportes/nota')

@login_required(login_url='/login')
def cancelar_reporte_usuario(request, id):
	reporte_usuario = ReporteUsuario.objects.get(id=id)
	reporte_usuario.delete()
	return HttpResponseRedirect('/lista/reportes/usuario')

@login_required(login_url='/login')
def nuevo_reporte_usuario(request):
	usuario_reportador = request.user
	usuario_reportado = Usuario.objects.get(id = int(request.POST['perfil_id']))
	tipo = request.POST['razon']
	descripcion = request.POST['descripcion']

	reporte_usuario = ReporteUsuario()
	reporte_usuario.usuario_reportador = usuario_reportador
	reporte_usuario.usuario_reportado = usuario_reportado
	reporte_usuario.tipo = tipo
	reporte_usuario.descripcion = descripcion

	reporte_usuario.save()
	num_reportes = ReporteUsuario.objects.filter(usuario_reportado = usuario_reportado).count()
	key_sesion = session_from_usuario(usuario_reportado.id)

	if (num_reportes >= MAX_REPORTES):
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		r.publish('usuario_reportado', '{"session_key": "' + str(key_sesion) + '" }')

		notify.send(
	            reporte_usuario,
	            description= reporte_usuario.usuario_reportado.username + ' ha sido reportado mas de '+str(MAX_REPORTES)+' veces ',
	            recipient=reporte_usuario.usuario_reportado,
	            target=reporte_usuario.usuario_reportador,
	            verb= 'usuario_reportado'
	        )

	return HttpResponseRedirect('/?mensaje=Reporte%20creado%20correctamente')

@login_required(login_url='/login')
def nuevo_post(request):
	p = True
	ctx = {}
	list_seguidores = '['
	if request.method == 'POST':
		form = NuevaNotaForm(request.POST, request.FILES)
		if form.is_valid():
			titulo = form.cleaned_data['titulo']
			descripcion = form.cleaned_data['descripcion']
			subseccion = form.cleaned_data['subseccion']
			privacidad = form.cleaned_data['privacidad']
			imagen = request.FILES['imagen']
			latitud = request.POST['latitud']
			longitud = request.POST['longitud']

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

			nota.longitud = longitud
			nota.latitud = latitud

			nota.save()
			helper.guardar_nota(nota)

			seguidores = UsuarioSigueUsuario.objects.filter(usuario_seguido = nota.usuario)
			seguidores_seccion = UsuarioSigueSeccion.objects.filter(seccion = nota.subseccion.seccion)

			for seguidor in seguidores:
				session_id = session_from_usuario(seguidor.usuario_seguidor.id)
				if session_id:
					list_seguidores = list_seguidores + '"' + session_id +'",'

			for seguidor in seguidores_seccion:
				session_id = session_from_usuario(seguidor.usuario.id)
				if session_id:
					list_seguidores = list_seguidores + '"' + session_id +'",'

			if len(list_seguidores) == 1:
				list_seguidores = "[]"
			else:
				list_seguidores = list_seguidores[:-1]
				list_seguidores = list_seguidores + "]"

			if ("." in descripcion):
				desc = descripcion[:descripcion.index('.')]
			else :
				desc = descripcion


			seccion_id = Subseccion.objects.get(id = nota.subseccion.id).seccion.id

			r = redis.StrictRedis(host='localhost', port=6379, db=1)
			r.publish('publicacion', '{ "seccion_id": "'+ str(seccion_id)+'", "titulo": "' + nota.titulo + '", "fecha": "' + naturaltime(nota.fecha) + '", "id": ' + str(nota.id) + ', "usuario_id":' + str(nota.usuario.id) + ', "latitud":' + str(nota.latitud) + ', "longitud":' + str(nota.longitud) + ', "descripcion": "'+ desc +'", "usuario": "'+ nota.usuario.username +'", "lista_usuarios": ' + list_seguidores + ' }')

			return HttpResponseRedirect('/?mensaje=Nota%20creada%20correctamente')

	else:
		form = NuevaNotaForm()

	ctx = {'form':form}
	return render(request,'nuevo_post.html',ctx)


def dejar_de_seguir_usuario_movil(request):
	id_usuario_seguidor = int(request.GET['id_seguidor'])
	id_usuario_seguido = int(request.GET['id_seguido'])

	usuario_seguido = Usuario.objects.get(id = id_usuario_seguido)
	usuario_seguidor = Usuario.objects.get(id = id_usuario_seguidor)

	u = UsuarioSigueUsuario.objects.get(usuario_seguido = usuario_seguido, usuario_seguidor = usuario_seguidor)
	u.delete()

	respuesta = {'mensaje': 'Usuario dejado de seguir'}

	return JsonResponse(respuesta, safe=False)

def dejar_de_seguir_seccion_movil(request):
	id_usuario_seguidor = int(request.GET['id_seguidor'])
	id_seccion = int(request.GET['id_seccion'])

	usuario_seguidor = Usuario.objects.get(id = id_usuario_seguidor)
	seccion = Seccion.objects.get(id = id_seccion)

	uss = UsuarioSigueSeccion.objects.get(seccion = seccion, usuario = usuario_seguidor)
	uss.delete()

	respuesta = {'mensaje': 'Seccion dejado de seguir'}

	return JsonResponse(respuesta, safe=False)

@csrf_exempt
def nuevo_post_movil(request):
	usuario_id = int(request.POST['usuario'])
	titulo = request.POST['titulo']
	descripcion = request.POST['descripcion']
	subseccion_id = int(request.POST['subseccion'])
	privacidad = True
	latitud = float(request.POST['latitud'])
	longitud = float(request.POST['longitud'])
	imagen = request.FILES['imagen']

	nota = Nota()
	nota.usuario = Usuario.objects.get(id = usuario_id)
	nota.titulo = titulo
	nota.descripcion = descripcion
	nota.subseccion = Subseccion.objects.get(id = subseccion_id)
	nota.privacidad = privacidad
	nota.imagen = imagen

	nota.longitud = longitud
	nota.latitud = latitud

	nota.save()
	helper.guardar_nota(nota)


	respuesta = {'id_nota': nota.id}

	return JsonResponse(respuesta, safe=False)

def lista_secciones_usuarios(request, id):
	secciones = list(UsuarioSigueSeccion.objects.filter(usuario=id).values())

	for seccion in secciones:
		seccion['nombre_seccion'] = Seccion.objects.get(id = seccion['seccion_id']).nombre
		seccion['username'] = Usuario.objects.get(id = seccion['usuario_id']).username

	return JsonResponse(secciones, safe=False)

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
					return HttpResponseRedirect('/?mensaje=Usuario%20creado%20con%20%C3%exito')
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
		form = EditarUsuarioForm(initial={
					'username': u.username,
					'nombre': u.nombre,
					'ap_paterno': u.ap_paterno,
					'ap_materno': u.ap_materno,
					'email': u.correo,
					#'bio': u.bio,
					'imagen': u.foto,
				})

	if request.method == 'POST':
		form = EditarUsuarioForm(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data['username']
			nombre = form.cleaned_data['nombre']
			ap_paterno = form.cleaned_data['ap_paterno']
			ap_materno = form.cleaned_data['ap_materno']
			email = form.cleaned_data['email']
			imagen = request.FILES['imagen']

			u.nombre = nombre
			u.ap_paterno = ap_paterno
			u.ap_materno = ap_materno
			u.username = username
			u.correo = email

			u.foto = imagen

			u.save()

			return HttpResponseRedirect('/perfil/' + str(u.id))

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
					'privacidad':privacidad,
					'latitud':nota.latitud,
					'longitud':nota.longitud
				})

	if request.method == 'POST':
		form = NuevaNotaForm(request.POST, request.FILES)
		if form.is_valid():
			titulo = form.cleaned_data['titulo']
			descripcion = form.cleaned_data['descripcion']
			subseccion = form.cleaned_data['subseccion']
			privacidad = form.cleaned_data['privacidad']
			latitud = request.POST['latitud']
			longitud = request.POST['longitud']
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

			nota.longitud = longitud
			nota.latitud = latitud

			nota.save()

			return HttpResponseRedirect('/?mensaje=Datos%20guardados%20correctamente')

	ctx = {'form':form}

	return render(request, 'editar_post.html', ctx)

@login_required(login_url='/login')
def eliminar_post(request, id):
	nota = Nota.objects.get(id = id)
	if(nota.usuario == request.user):
		nota.delete()		

	return HttpResponseRedirect('/?mensaje=Nota%20eliminada%20correctamente')

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
					return HttpResponseRedirect('/?mensaje=Conectado')
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


def encuentra_nota(request):
	palabra = request.GET['q']
	lista_noticias = Nota.objects.filter(Q(descripcion__contains=palabra) | Q(titulo__contains=palabra) | Q(titulo__contains=palabra)).order_by('-id')

	lista_noticias = list(lista_noticias.values())

	for noticia in lista_noticias:
		usuario = Usuario.objects.get(id = noticia['usuario_id'])
		noticia['usuario'] = {
			'username': usuario.username,
			'id': usuario.id
		}
		noticia['seccion_id'] = Subseccion.objects.get(id = noticia['subseccion_id']).seccion.id


	paginator = Paginator(lista_noticias, 6)
 	page = request.GET.get('page')
 	try:
		noticias = paginator.page(page)
 	except PageNotAnInteger:
		noticias = paginator.page(1)
	except EmptyPage:
		noticias = paginator.page(paginator.num_pages)

	ctx = {'noticias': noticias, 'q': palabra}
	return render(request, 'index.html', ctx)

def encuentra_reporte_nota(request):
	palabra = request.GET['q']

	reportes = ReporteNota.objects.filter(Q(descripcion__contains=palabra) | Q(tipo__contains=palabra))

	reportes = reportes.annotate(num_reportes=Count('id')).filter(num_reportes__gte=MAX_REPORTES)
	last_date = datetime.today() - timedelta(weeks=CADUCA_REPORTES)

	paginator = Paginator(reportes, 8)
 	page = request.GET.get('page')
 	try:
		reportes_nota = paginator.page(page)
 	except PageNotAnInteger:
		reportes_nota = paginator.page(1)
	except EmptyPage:
		reportes_nota = paginator.page(paginator.num_pages)

	reportes_pasados = ReporteNota.objects.all().annotate(num_reportes=Count('id')).filter(num_reportes__gte=MAX_REPORTES).filter(fecha__lte = last_date)

	ctx = {'reportes_nota': reportes_nota, 'nombre_vista': 'Lista de Reportes de Notas', 'reportes_pasados': reportes_pasados, 'q': palabra}
	return render(request, 'reportes.html', ctx)

def encuentra_reporte_usuario(request):
	palabra = request.GET['q']

	reportes = ReporteUsuario.objects.filter(Q(descripcion__contains=palabra) | Q(tipo__contains=palabra))
	reportes = list(reportes.annotate(num_reportes=Count('id')).filter(num_reportes__gte=MAX_REPORTES))
	last_date = datetime.today() - timedelta(weeks=CADUCA_REPORTES)

	paginator = Paginator(reportes, 8)
 	page = request.GET.get('page')
 	try:
		reportes_usuario = paginator.page(page)
 	except PageNotAnInteger:
		reportes_usuario = paginator.page(1)
	except EmptyPage:
		reportes_usuario = paginator.page(paginator.num_pages)

	reportes_pasados = ReporteUsuario.objects.filter(fecha__lte = last_date)

	ctx = {'reportes_usuario': reportes_usuario, 'nombre_vista': 'Lista de Reportes de Usuario', 'reportes_pasados': reportes_pasados, 'q': palabra}
	return render(request, 'reportes_usuarios.html', ctx)


#Ajax
@csrf_exempt
def editar_usuario_movil(request):
	u = Usuario.objects.get(id = int(form.cleaned_data['id']))
	username = form.cleaned_data['username']
	nombre = form.cleaned_data['nombre']
	ap_paterno = form.cleaned_data['ap_paterno']
	ap_materno = form.cleaned_data['ap_materno']
	email = form.cleaned_data['email']
	imagen = request.FILES['imagen']

	u.nombre = nombre
	u.ap_paterno = ap_paterno
	u.ap_materno = ap_materno
	u.username = username
	u.correo = email

	u.foto = imagen

	if u.save():
		return JsonResponse({'mensaje': 'Usuario editado correctamente', 'id': u.id}, safe=False)
	else:
		return JsonResponse({'mensaje': 'Usuario no ha sido editado correctamente', 'id': u.id}, safe=False)

def comentarios_noticias(request, id):
	nota = Nota.objects.get(id = id)
	comentarios = list(Comentario.objects.filter(nota = nota).order_by('-fecha').values())

	return JsonResponse(comentarios, safe=False)

def like_movil(request):
	id_usuario = request.GET['id_usuario']
	id_nota = request.GET['id_nota']
	le_gusta = request.GET['like']

	usuario = Usuario.objects.get(id = id_usuario)
	nota = Nota.objects.get(id = id_nota)

	if le_gusta == 'true':
		like = LikeNota.objects.get(usuario = usuario, nota = nota)
		like.delete()
	else:
		like = LikeNota()
		like.nota = nota
		like.usuario = usuario
		like.save()

		if (nota.usuario.id != request.user.id):
			key_sesion = session_from_usuario(nota.usuario.id)
			r = redis.StrictRedis(host='localhost', port=6379, db=2)
			mensaje = '{ "session_key": "' + str(key_sesion) + '", "usuario": "' + usuario.username + '", "nota_id": ' + str(nota.id) + ', "nota": "' + nota.titulo + '" }'
			r.publish('me_gusta', mensaje)

			notify.send(
		            like,
		            description= usuario.username + ' le ha gustado ' + nota.titulo,
		            recipient=nota.usuario,
		            target=nota,
		            verb= 'nuevo_like'
		        )

	respuesta = {'usuario': usuario.username, 'titulo': nota.titulo}
	return JsonResponse(respuesta, safe=False)


def editar_nota_movil(request):
	nota = Nota.objects.get(id = int(form.cleaned_data['id']))
	titulo = form.cleaned_data['titulo']
	descripcion = form.cleaned_data['descripcion']
	subseccion = form.cleaned_data['subseccion']
	privacidad = form.cleaned_data['privacidad']
	latitud = form.cleaned_data['latitud']
	longitud = form.cleaned_data['longitud']
	imagen = request.FILES['imagen']

	nota.usuario = request.user
	nota.titulo = titulo
	nota.descripcion = descripcion
	nota.subseccion = subseccion
	nota.privacidad = p
	nota.imagen = imagen
	nota.latitud = latitud
	nota.longitud = longitud

	if nota.save():
		return JsonResponse({'mensaje': 'Nota editada correctamente', 'id': nota.id}, safe=False)
	else:
		return JsonResponse({'mensaje': 'Nota no ha sido editada correctamente', 'id': nota.id}, safe=False)


def mensajes_chat(request, id):
	chat = Chat.objects.get(id=id)
	mensajes_directos = list(MensajeDirecto.objects.filter(chat = chat).values())

	for mensaje in mensajes_directos:
		mensaje['fecha'] = naturaltime(mensaje['fecha'])

	return JsonResponse(mensajes_directos, safe=False)

def chats_usuario(request, id):
	user = Usuario.objects.get(id=id)
	chats = list(Chat.objects.filter(Q(usuario_uno = user) | Q(usuario_dos = user)).values())

	return JsonResponse(chats, safe=False)

def novedades(request):
	last_day = datetime.today() - timedelta(days=1)	
	novedades = Nota.objects.filter(fecha__gte = last_day).order_by('-fecha')[:4]
	lista_likes = []

	for publicacion in novedades:
		num_likes = LikeNota.objects.filter(nota = publicacion).count()
		lista_likes.append({'nota':publicacion,'num_likes': num_likes})

	novedades = sorted(lista_likes, key=lambda k: k['num_likes'], reverse=True)

	return JsonResponse(novedades, safe=False)

def usuarios_populares(request):
	id_usuarios = []
	last_day = datetime.today() - timedelta(days=1)	
	novedades = Nota.objects.filter(fecha__gte = last_day).order_by('-fecha')[:4]
	lista_likes = []

	for publicacion in novedades:
		num_likes = LikeNota.objects.filter(nota = publicacion).count()
		lista_likes.append({'nota':publicacion,'num_likes': num_likes})

	novedades = sorted(lista_likes, key=lambda k: k['num_likes'], reverse=True)
	
	for novedad in novedades:
		id_usuarios.append(novedad['nota'].usuario.id)

	usuarios_populares = list(Usuario.objects.filter(id__in=id_usuarios).values())

	return JsonResponse(usuarios_populares, safe=False)

def ver_usuario(request, username):
	usuarios = Usuario.objects.filter(username = username)
	if (usuarios):
		usuario = usuarios.get()
		respuesta = {'id_usuario': usuario.id,'username': usuario.username, 'nombre': usuario.nombre,'apellidos': usuario.ap_paterno + ' ' + usuario.ap_materno, 'foto': str(usuario.foto)}
	else:
		respuesta = {'mensaje': 'El usuario no existe'}

	return JsonResponse(respuesta, safe=False)

@csrf_exempt
def lista_notas_usuarios_ajax(request, username):
	usuarios = Usuario.objects.filter(username = username)
	if (usuarios):
		usuario = usuarios.get()
		respuesta = list(Nota.objects.filter(usuario=usuario).order_by('-fecha').values())
	else:
		respuesta = {'mensaje': 'El usuario no existe'}

	return JsonResponse(respuesta, safe=False)

@csrf_exempt
def lista_notas_seccion_ajax(request, id):
	seccion = Seccion.objects.get(id = id)
	subseccion = Subseccion.objects.filter(seccion = seccion)

	respuesta = list(Nota.objects.filter(subseccion=subseccion).order_by('-fecha').values())
	return JsonResponse(respuesta, safe=False)

def lista_seguidores_ajax(request, id):
	lista_seguidores = list(UsuarioSigueUsuario.objects.filter(usuario_seguido = id).values())

	return JsonResponse(lista_seguidores, safe=False)

def lista_seguidos_ajax(request, id):
	lista_seguidos = list(UsuarioSigueUsuario.objects.filter(usuario_seguidor = id).values())

	return JsonResponse(lista_seguidos, safe=False)	

def get_chat(request):
	usuario = request.GET.get('usuario_consultor', None)
	usuario_chat = request.GET.get('usuario_chat', None)

	mensajes = list(MensajeDirecto.objects.filter(Q(usuario_remitente = usuario, usuario_destinatario = usuario_chat) | Q(usuario_remitente = usuario_chat, usuario_destinatario = usuario)).values().order_by('-fecha'))

	for mensaje in mensajes:
		mensaje['fecha'] = naturaltime(mensaje['fecha']);

	return JsonResponse(mensajes, safe=False)

def get_chat_id(request, id):
	usuario = request.user
	usuario_chat = Usuario.objects.get(id = id)

	chats = Chat.objects.filter(Q(usuario_uno = request.user) | Q(usuario_dos = request.user))
	chats = chats.filter(Q(usuario_uno = usuario_chat) | Q(usuario_dos = usuario_chat))		

	if (chats):
		return JsonResponse({'id': chats.get().id})	
	else:
		chat = Chat()
		chat.usuario_uno = usuario
		chat.usuario_dos = usuario_chat

		chat.save()
		return JsonResponse({'id': chat.id})

def get_puntos(request):
	last_day = datetime.today() - timedelta(days=1)

	if request.user.is_authenticated():
		siguiendo_seccion_id = UsuarioSigueSeccion.objects.filter(usuario = request.user).values_list('seccion', flat=True)
		subsecciones_id = Subseccion.objects.filter(seccion = siguiendo_seccion_id).values_list('id', flat=True)
		siguiendo_id = UsuarioSigueUsuario.objects.filter(usuario_seguidor = request.user).values_list('usuario_seguido', flat=True)
		lista_noticias = Nota.objects.filter((Q(usuario = siguiendo_id) | Q(usuario = request.user) | Q(subseccion = subsecciones_id)), fecha__gte=last_day).order_by('-id')
	else:
		lista_noticias = Nota.objects.filter(fecha__gte = last_day)


	lista_noticias = list(lista_noticias.values())	

	notas = list(Nota.objects.filter(fecha__gte = last_day).values())
	notas_result = helper.obtener_notas_loc(request.GET['lon'] ,request.GET['lat'], notas)


	for nota in lista_noticias:
		nota['seccion_id'] = Subseccion.objects.get(id = nota['subseccion_id']).seccion.id

	for nota in notas_result:
		nota['seccion_id'] = Subseccion.objects.get(id = nota['subseccion_id']).seccion.id

	result = {
		'lista_noticias': lista_noticias,
		'notas_result': notas_result
	}

	return JsonResponse(result, safe=False)


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

	key_sesion = session_from_usuario(nota.usuario.id)

	r = redis.StrictRedis(host='localhost', port=6379, db=2)
	mensaje = '{ "session_key": "' + str(key_sesion) + '", "usuario": "' + comentario.usuario.username + '", "contenido": "' + comentario.contenido + '", "nota_id": ' + str(comentario.nota.id) + ', "nota": "' + comentario.nota.titulo + '", "fecha": "' + naturaltime(comentario.fecha) + '" }'
	r.publish('comentario', mensaje)

	if (request.user != nota.usuario):
		notify.send(
	            comentario,
	            description= usuario.username + ' ha hecho un comentario nuevo en ' + comentario.nota.titulo,
	            recipient=comentario.nota.usuario,
	            target=nota,
	            verb= 'nuevo_comentario'
	        )

	comentario_json = {'comentario_id': comentario.id, 'contenido': comentario.contenido, 'usuario': usuario.username, 'imagen': str(usuario.foto)}

	return JsonResponse(comentario_json, safe=False)

def eliminar_comentario(request, id):
	comentario = Comentario.objects.get(id = id)
	nota_id = comentario.nota.id
	comentario.delete()	

	return HttpResponseRedirect('/publicacion/' + str(nota_id))

@csrf_exempt
def nuevo_mensaje(request):
	usuario_remitente = Usuario.objects.get(id = int(request.POST['usuario_consultor']))
	usuario_destinatario = Usuario.objects.get(id = int(request.POST['usuario_chat']))
	mensaje = request.POST['mensaje']
	id_chat = request.POST['id_chat']

	chat = Chat.objects.get((Q(usuario_uno = usuario_remitente) | Q(usuario_dos = usuario_remitente)), (Q(usuario_uno = usuario_destinatario) | Q(usuario_dos = usuario_destinatario)))

	mensaje_directo = MensajeDirecto()
	mensaje_directo.usuario_remitente = usuario_remitente
	mensaje_directo.usuario_destinatario = usuario_destinatario
	mensaje_directo.contenido = mensaje
	mensaje_directo.chat = chat

	mensaje_directo.save()

	#Once comment has been created post it to the chat channel
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	r.publish('chat', '{ "contenido": "' + mensaje_directo.contenido + '", "fecha": "' + naturaltime(mensaje_directo.fecha) + '", "id": ' + str(mensaje_directo.id) + ', "usuario_remitente": '+ str(usuario_remitente.id) +', "id_chat": "'+ str(id_chat) +'" }')

	comentario_json = {'contenido': mensaje_directo.contenido, 'fecha': naturaltime(mensaje_directo.fecha), 'id': mensaje_directo.id}

	return JsonResponse(comentario_json, safe=False)

def eliminar_mensaje(request):
	MensajeDirecto.objects.get(id = int(request.GET['id'])).delete()

	comentario_json = {'mensaje': 'Eliminado satisfactoriamente'}

	return JsonResponse(comentario_json, safe=False)

def like(request):

	id_post = request.GET['id_post']
	id_usuario = request.GET['id_usuario']

	le_gusta = request.GET['like']
	usuario = Usuario.objects.get(id = id_usuario)
	nota = Nota.objects.get(id = id_post)

	if le_gusta == 'true':
		like = LikeNota.objects.get(usuario = usuario, nota = nota)
		like.delete()
	else:
		like = LikeNota()
		like.nota = nota
		like.usuario = usuario
		like.save()

		if (nota.usuario.id != request.user.id):
			key_sesion = session_from_usuario(nota.usuario.id)
			r = redis.StrictRedis(host='localhost', port=6379, db=2)
			mensaje = '{ "session_key": "' + str(key_sesion) + '", "usuario": "' + usuario.username + '", "nota_id": ' + str(nota.id) + ', "nota": "' + nota.titulo + '" }'
			r.publish('me_gusta', mensaje)

			notify.send(
		            like,
		            description= usuario.username + ' le ha gustado ' + nota.titulo,
		            recipient=nota.usuario,
		            target=nota,
		            verb= 'nuevo_like'
		        )

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

	session_key = session_from_usuario(id)

	if session_key:
		r = redis.StrictRedis(host='localhost', port=6379, db=3)
		mensaje = '{ "seguidor": "' + request.user.username + '", "seguidor_id": ' + str(request.user.id) + ', "session_key":"' + session_key + '"}'

		r.publish('nuevo_seguidor', mensaje)

	usu.save()

	notify.send(
	        usu,
	        description= usu.usuario_seguidor.username + ' te ha seguido ',
	        recipient=usu.usuario_seguido,
	        target=usu.usuario_seguidor,
	        verb= 'nuevo_seguidor'
	    )
	
	return HttpResponseRedirect('/perfil/' + str(id))

def seguir_seccion(request, id):
	usuario = request.user
	seccion = Seccion.objects.get(id = id)

	uss = UsuarioSigueSeccion()
	uss.usuario = usuario
	uss.seccion = seccion

	uss.save()

	return HttpResponseRedirect('/lista/nota/seccion/' + str(id))

def dejar_de_seguir_seccion(request, id):
	seccion = Seccion.objects.get(id = id)
	usuario = request.user
	uss = UsuarioSigueSeccion.objects.get(seccion = seccion, usuario = usuario)
	uss.delete()

	return HttpResponseRedirect('/lista/nota/seccion/' + str(id))

#Administracion
def dar_de_baja_nota(request, id):
	nota = Nota.objects.get(id = id)
	nota.delete()

	return HttpResponseRedirect('/lista/reportes/nota')

def dar_de_baja_usuario(request, id):
	usuario = Usuario.objects.get(id = id)
	usuario.delete()

	return HttpResponseRedirect('/lista/reportes/usuario')


#Notificaciones
def eliminar_notificacion(request, id):
	notificacion = Notification.objects.get(id = id)
	notificacion.delete()

	return HttpResponseRedirect('/lista/notificaciones')

def leer_notificacion(request, id):
	notificacion = Notification.objects.get(id = id)
	notificacion.unread = False

	notificacion.save()

	return HttpResponseRedirect('/lista/notificaciones')
