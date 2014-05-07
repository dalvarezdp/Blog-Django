from principal.models import Entrada, Comentario
from principal.forms import EntradaForm, ComentarioForm, ContactoForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def sobre(request):
	html = "<html><body>Trabajo realizado por: <b>David Alvarez del Pino</b></body></html>"
	return HttpResponse(html)


def usuarios(request):
	usuarios = User.objects.all()
	entradas = Entrada.objects.all()
	return render_to_response('usuarios.html',{'usuarios':usuarios,'entradas':entradas}, context_instance=RequestContext(request))

def lista_entradas(request):
	usuario=request.user
	entradas = Entrada.objects.all()
	if usuario.is_authenticated():
		return render_to_response('privado.html',{'usuario':usuario,'datos':entradas}, context_instance=RequestContext(request))
	else:
		return render_to_response('inicio.html',{'usuario':usuario,'datos':entradas}, context_instance=RequestContext(request))

def detalle_entrada(request, id_entrada):
	usuario=request.user
	dato = get_object_or_404(Entrada, pk=id_entrada)
	comentarios = Comentario.objects.filter(entrada=dato)
	if request.method=='POST':
		formulario=ComentarioForm(request.POST)
		if formulario.is_valid():
			f=formulario.save(commit=False)
			f.entrada=dato		
			if not request.user.is_anonymous():
				f.usuario=usuario
			else:
				try:
					anonimo = User.objects.get(username='Anonimo')
				except User.DoesNotExist:
					anonimo = User.objects.create_user('Anonimo','','')
				f.usuario=anonimo
			f.save()
			#return HttpResponseRedirect(reverse('detalle_entrada',args=[id_entrada]))
			return HttpResponseRedirect('/')
	else:
		formulario = ComentarioForm()
		if not usuario.is_anonymous():
			return render_to_response('entrada_privado.html',{'usuario':usuario,'entrada':dato,'comentarios':comentarios,'formulario':formulario}, context_instance=RequestContext(request))
		else:
			return render_to_response('entrada.html',{'usuario':usuario,'entrada':dato,'comentarios':comentarios,'formulario':formulario}, context_instance=RequestContext(request))
		


def contacto(request):
	if request.method=='POST':
		formulario=ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mensaje desde el blog'
			contenido = formulario.cleaned_data['mensaje']+"\n"
			contenido += 'Comunicarse a: '+ formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['i92alpid@uco.es'])
			correo.send()
			return HttpResponseRedirect('/')
	else:
		formulario = ContactoForm()
	return render_to_response('contactoform.html',{'formulario':formulario}, context_instance=RequestContext(request))


def nueva_entrada(request):
	usuario=request.user
	if request.method=='POST':
		formulario=EntradaForm(request.POST, request.FILES)
		if formulario.is_valid():
			f=formulario.save(commit=False)
			f.votos=0
			f.usuario=usuario
			f.save()
			return HttpResponseRedirect('/')
	else:
		formulario = EntradaForm()
	return render_to_response('entradaform.html',{'formulario':formulario}, context_instance=RequestContext(request))


def nuevo_comentario(request):
	if request.method=='POST':
		formulario=ComentarioForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/inicio')
	else:
		formulario = ComentarioForm()
	return render_to_response('comentarioform.html',{'formulario':formulario}, context_instance=RequestContext(request))


def nuevo_usuario(request):
	if request.method == 'POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = UserCreationForm()
	return render_to_response('nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario,password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def privado(request):
	usuario=request.user
	entradas = Entrada.objects.all()
	return render_to_response('privado.html',{'usuario':usuario,'datos':entradas}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

def borrar_entrada(request, id_entrada):
	entrada = Entrada.objects.get(pk=id_entrada)
	entrada.delete()
	return HttpResponseRedirect('/')

def modificar_entrada(request, id_entrada):
	entrada = Entrada.objects.get(pk=id_entrada)
	if request.method == 'POST':
		formulario = EntradaForm(request.POST, request.FILES, instance=entrada)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = EntradaForm(instance=entrada)
	return render_to_response('modificar_entrada.html', {'formulario':formulario}, context_instance=RequestContext(request))


def borrar_comentario(request, id_comentario):
	comentario = Comentario.objects.get(pk=id_comentario)
	comentario.delete()
	return HttpResponseRedirect('/')



def modificar_comentario(request, id_comentario):
	comentario = Comentario.objects.get(pk=id_comentario)
	if request.method == 'POST':
		formulario = ComentarioForm(request.POST, instance=comentario)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = ComentarioForm(instance=comentario)
	return render_to_response('modificar_comentario.html', {'formulario':formulario}, context_instance=RequestContext(request))


def perfil(request):
	usuario=request.user
	entradas = Entrada.objects.all()
	comentarios = Comentario.objects.all()
	return render_to_response('perfil.html',{'usuario':usuario,'entradas':entradas,'comentarios':comentarios}, context_instance=RequestContext(request))


def voto_positivo(request, id_entrada):
	usuario=request.user
	entrada = Entrada.objects.get(pk=id_entrada)
	entrada.votos += 1
	entrada.save()
	entradas = Entrada.objects.all()
	return render_to_response('inicio.html', {'usuario':usuario,'datos':entradas}, context_instance=RequestContext(request))


def voto_negativo(request, id_entrada):
	usuario=request.user
	entrada = Entrada.objects.get(pk=id_entrada)
	entrada.votos -= 1
	entrada.save()
	entradas = Entrada.objects.all()
	return render_to_response('inicio.html', {'usuario':usuario,'datos':entradas}, context_instance=RequestContext(request))


def adminusuarios(request):
	usuario=request.user
	if usuario.is_staff:
		users = User.objects.all()
		return render_to_response('adminusuarios.html', {'usuarios':users}, context_instance=RequestContext(request))

def staff(request, id_usuario):
	usuario=request.user
	if usuario.is_staff:
		usuarios = User.objects.get(pk=id_usuario)
		usuarios.is_staff = 1
		usuarios.save()
		users = User.objects.all()
		return render_to_response('adminusuarios.html', {'usuarios':users}, context_instance=RequestContext(request))

def nostaff(request, id_usuario):
	usuario=request.user
	if usuario.is_staff:
		usuarios = User.objects.get(pk=id_usuario)
		usuarios.is_staff = 0
		usuarios.save()
		users = User.objects.all()
		return render_to_response('adminusuarios.html', {'usuarios':users}, context_instance=RequestContext(request))


