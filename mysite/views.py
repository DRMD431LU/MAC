from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from PagGestion.models import Encuesta_Profesor, Encuesta_Alumno,Profesor
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render_to_response

def hola(request):
    return HttpResponse("Hola Mundo")
def fecha_actual(request):
    ahora = datetime.datetime.now()
    html = "<html><body><h1>Fecha:</h1><h3>%s<h/3></body></html>" % ahora
    return HttpResponse(html)

def encuesta_profesores(request):
    contenido =Encuesta_Profesor.objects.all()
    return render_to_response('encuesta_profesores.html', {"results":contenido})
def encuesta_alumnos(request):
    contenido =Encuesta_Alumno.objects.all()
    return render_to_response('encuesta_alumnos.html', {"results":contenido})
def asignacion(request):
    contenido=Profesor.objects.all()
    return render_to_response('asignacion_profesor.html', {"results":contenido})

def index(request):
    messages.success(request,"Hola, Bienvenidos al SGC UTLA.")
    return render(request,'index.html')
