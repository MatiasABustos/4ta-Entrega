from django.shortcuts import render
from AppCoder.models import Curso, Avatar
from django.http import HttpResponse
from django.template import loader
from AppCoder.forms import Curso_formulario, UserEditForm
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def inicio(request):
    return render(request , "padre.html")

def alta_curso(request,nombre):
    curso = Curso(nombre= nombre , camada=23456, nivel= "medio")
    curso.save()
    texto = f"Se guardó en la BD el curso: {curso.nombre} {curso.camada} {curso.nivel}"
    return HttpResponse(texto)

@login_required
def ver_cursos(request):
    cursos = Curso.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "cursos.html", {"url":avatares[0].imagen.url , "cursos":cursos})

@login_required
def alumnos(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request , "alumnos.html", {"url":avatares[0].imagen.url , "alumnos":alumnos})

@login_required
def profesores(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request,"profesores.html", {"url":avatares[0].imagen.url , "profesores":profesores})

def curso_formulario(request):

    if request.method == "POST":

        mi_formulario = Curso_formulario( request.POST )

        if mi_formulario.is_valid(): #aca valido la criteria del form
            datos = mi_formulario.cleaned_data 

            curso =  Curso( nombre=datos['nombre'] , camada=datos['camda'] , nivel=datos['nivel'])
            curso.save()
            return render(request, "formulario.html")

    return render(request, "formulario.html")


def buscar_curso(request):
    return render(request, "buscar_curso.html")


def buscar(request):

    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        curso = Curso.objects.filter(nombre__icontains= nombre)
        return render(request, "resultado_busqueda.html" , {"curso":curso})
    else:
        return HttpResponse("Ingresa el nombre del curso")
    

def elimina_curso(request, id):
    curso = Curso.objects.get(id=id)
    curso.delete()

    curso = Curso.objects.all()

    return render(request, "curso.html", {"cursos:curso"})

def editar(request, id):

    curso = Curso.objects.get(id=id)

    if request.method == "POST":
        
        mi_formulario = Curso_formulario( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos["nombre"]
            curso.camada = datos["camada"]
            curso.nivel = datos["nivel"]
            curso.save()

            curso = Curso.objects.all()
            
            return render(request , "cursos.html" , {"cursos":curso})

    else:
        mi_formulario = Curso_formulario(initial={"nombre":curso.nombre , "camada":curso.camada, "nivel":curso.nivel})
    
    return render(request, "editar_curso.html" , {"mi_formulario": mi_formulario , "curso":curso})

def login_request(request):
    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario , password=contra)

            if user is not None:
                login(request, user )
                avatares = Avatar.objects.filter(user=request.user.id)
                return render(request , "inicio.html", {"url":avatares[0].imagen.url, "mensaje":f"Bienvenido/a {usuario}", "usuario":usuario})
            else:
                return HttpResponse(f"Usuario no encontrado")
        else:
            return HttpResponse(f"FORM INCORRECTO {form}")

    form = AuthenticationForm()
    return render( request , "login.html" , {"form":form})


def register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse("Usuario creado")
    
    else:
        form = UserCreationForm()
    return render(request, "registro.html" , {"form":form})



def editarPerfil(request):
    usuario = request.user

    if request.method == "POST":
        mi_formulario = UserEditForm(request.POST)
        if mi_formulario.is_valid():

            informacion = mi_formulario.cleaned_data
            usuario.email = informacion["email"]
            password = informacion["password1"]
            usuario.set_password(password)
            usuario.save()
            return render(request , "inicio.html")
    else:
        miFormulario = UserEditForm(initial={'email':usuario.email})
    
    return render(request, "editar_perfil.html", {"miFormulario":miFormulario, "usuario":usuario})
