# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#noip
from django.shortcuts import render
from .models import Profesor,Practica,Fecha_Limite,Agenda_Practica,Horario,Dia_No_Laborable,Turno,Grupos_Carrera,Materia_Laboratorio,Laboratorio_Horario,Dias,Carrera,Alumno,Generacion,Alumno_Inscrito,Periodo
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from .forms import UploadForm
import time, datetime
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str,smart_text
from django.contrib.auth.models import User
from datetime import datetime,timedelta
#mandar librería a John
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView
from PagGestion.forms import Agenda_PracticaForm
from django.core.urlresolvers import reverse_lazy
import pandas as pd
from PagGestion.forms import UploadForm,Agenda_PracticaForm
from tablib import Dataset
import csv
import io

# Create your views here.
from django.views.generic import ListView



def profesores_upload(request):
    c=0
    first=True
    if request.method=='POST':

                form=UploadForm(request.POST,request.FILES)
                if form.is_valid():
                    archivo=request.FILES['f'].read().decode('utf-8')

                    new_profesor=Profesor()
                    lineas=archivo.split('\n')

                    for row in lineas:

                        if first is not True:
                            columnas=row.split(',')

                            if columnas[0] != '':
                                try:
                                    rfc_b=Profesor.objects.get(rfc=columnas[0])
                                except Profesor.DoesNotExist:
                                    rfc_b=None

                                if rfc_b is None:
                                    new_profesor.rfc=columnas[0]
                                    new_profesor.homoclave=columnas[1]
                                    new_profesor.nombre=columnas[2]
                                    new_profesor.num_empleado=columnas[3]
                                    new_profesor.curp=columnas[4]
                                    try:
                                        id_carrera_base=Carrera.objects.get(Nombre=columnas[5])
                                    except Carrera.DoesNotExist:
                                        id_carrera_base=None

                                    new_Carrera=Carrera()
                                    if id_carrera_base is None:
                                        new_Carrera.clave="Dummy"
                                        new_Carrera.Nombre=columnas[5]
                                        new_Carrera.save()
                                    id_carrera_base=Carrera.objects.get(Nombre=columnas[5])
                                    new_profesor.id_carrera=id_carrera_base
                                    new_profesor.correo_e=columnas[6]
                                    new_profesor.save()
                                    crear_usuario(columnas[0],columnas[6],columnas[7])
                                    c+=1
                        first=False
                        form=UploadForm()

    else:
        form=UploadForm()
    return render(request,'importar_Profesores.html',{'form':form,'c':c,'first':first})

def horarios_profesores_upload(request):
        c=0
        first=True
        if request.method=='POST':
            form=UploadForm(request.POST,request.FILES)
            if form.is_valid():
                archivo=request.FILES['f'].read().decode('utf-8')
                new_profesor=Profesor()
                lineas=archivo.split('\n')
                for row in lineas:
                    if first is not True:
                        columnas=row.split(',')
                        if columnas[0] != '' and 'LAB' in columnas[1].upper():
                            c=crear_materia_laboratorio(columnas,nombre_carrera,encabezados,c)
                    else:
                        nombre_carrera=cargar_catalogos_para_profesores(row.split(','),request.FILES['f'])
                        encabezados=row.split(',')
                        first=False
                    form=UploadForm()
        else:
            form=UploadForm()
        return render(request,'importar_Profesores.html',{'form':form,'c':c,'first':first})

def cargar_catalogos_para_profesores(rows,archivo):
        s1=archivo.name.replace('Profesores.csv','').replace('_',' ').split()
        nombre_archivo=" ".join(s1)
        Carrera.objects.get_or_create(clave='Dummy',Nombre=nombre_archivo)
        for x in range(11,17):
            Dias.objects.get_or_create(dias=rows[x])
        return nombre_archivo

def crear_materia_laboratorio(columnas,nombre_carrera,encabezados,c):
    id_carrera=Carrera.objects.get(Nombre=nombre_carrera)
    profesor,_=Profesor.objects.get_or_create(
        rfc=columnas[5],nombre=columnas[4],num_empleado=columnas[21],
        id_carrera=id_carrera,correo_e=columnas[20],telefono_casa=columnas[18],
        telefono_oficina=columnas[19])
    materia,_=Materia_Laboratorio.objects.get_or_create(
        clave=columnas[0],nombre=columnas[1].replace('(LAB)','').replace('(Lab)',''),
        id_carrera=id_carrera)
    turno,_=Turno.objects.get_or_create(clave=columnas[2][0],valor=("Matutino" if columnas[2][0]=='0' else "Vespertino"))
    grupo,_=Grupos_Carrera.objects.get_or_create(
        clave=columnas[2],id_carrera=id_carrera,
        id_turno=Turno.objects.get(clave=columnas[2][0])
    )
    periodo=Periodo.objects.get(activo=True)
    lab_hora,created=Laboratorio_Horario.objects.get_or_create(
        rfc=profesor,
        id_grupo=grupo,
        id_clave_mat_lab=materia,
        periodo=periodo,
    )
    crear_h_d_d(columnas,encabezados,lab_hora)
    if created:
        c+=1
        crear_usuario(columnas[5],columnas[20],columnas[22])
    return c

def crear_h_d_d(columnas,encabezados,lab_hora):
    print(columnas,encabezados)
    for x in range(11,17):
        if len(columnas[x])>1:
            id_dias=Dias.objects.get(dias=encabezados[x])
            hora=columnas[x].split()
            h_i,_=Horario.objects.get_or_create(hora=hora[0])
            h_f,_=Horario.objects.get_or_create(hora=hora[1])
            Horarios_Clase.objects.get_or_create(
                laboratorio_horario=lab_hora,
                id_dias=id_dias,
                hora_ini=h_i,
                hora_fin=h_f
            )

def cargar_alumnos(request):
    c=0
    first=True
    if request.method=='POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            archivo=request.FILES['f'].read().decode('utf-8')
            new_alumno=Alumno()
            lineas=archivo.split('\n')
            s1=request.FILES['f'].name.replace('Alumnos.csv','').replace('_',' ').split()
            nombre_carrera=" ".join(s1)
            for row in lineas:
                if first is True:
                    encabezados=row.split(',')
                    first=False
                else:
                    columnas=row.split(',')
                    if columnas[0] != '':
                        c=crear_alumno_inscrito(columnas,nombre_carrera,encabezados,c)
                form=UploadForm()
    else:
        form=UploadForm()
    return render(request,'importar_horarios.html',{'form':form,'c':c,'first':first})

def crear_alumno_inscrito(columnas,nombre_carrera,encabezados,c):
    id_carrera=get_object_or_404(Carrera,Nombre=nombre_carrera)
    generacion,_=Generacion.objects.get_or_create(valor=columnas[5])
    alumno,_=Alumno.objects.get_or_create(num_cuenta=columnas[1],
    nombre=columnas[0],id_generacion=generacion,id_carrera=id_carrera,
    email=columnas[6],fecha_nac=datetime.strptime(columnas[7],"%Y/%m/%d").date())
    crear_usuario(alumno.num_cuenta,alumno.email,datetime.strftime(alumno.fecha_nac,"%d%m%Y"))
    grupo=columnas[3].split()[0]
    clave_materia=columnas[2]+"L"
    created=False
    try:
        id_laboratorio_horario=Laboratorio_Horario.objects.get(
            id_grupo=grupo,
            id_clave_mat_lab=clave_materia,
            periodo__activo=True)
        _,created=Alumno_Inscrito.objects.get_or_create(
            id_alumno=alumno,
            id_laboratorio_horario=id_laboratorio_horario)
    except Laboratorio_Horario.DoesNotExist:
        x=2
    if created:
        c+=1
    return c

def crear_usuario(usuario,email,password):
    user,created = User.objects.get_or_create(username=usuario,email=email)
    if not created:
        user.set_password(password)
    user.save()


def acciones(request):
    #mandar a john este mensaje
        messages.success(request,"Hola, Bienvenidos.")
        return render(request,'Acciones.html')
def encuesta_laboratorio(request):
        messages.success(request,"Hola, Bienvenidos.")
        return render(request,'cuestionario_laboratorio.html')
def encuesta_practica(request):
        messages.success(request,"Hola, Bienvenidos.")
        return render(request,'cuestionario_practica.html')

def agenda_profesores(request):
    form =Agenda_PracticaForm()
    f2=UploadForm()
    contenido =Agenda_Practica.objects.all()
    messages.success(request,"Consulta de Agenda Lista.")
    return render(request,'agenda_profesores.html',{'result':contenido,'form':form,'f2':f2})

def generar_agenda(request):
    dias_limite=Fecha_Limite.objects.filter(id_tipo__nombre="R_P").values('id_clase_tipo__nombre','fecha')

    fp=pd.DataFrame(list(dias_limite))
    inicio=fp[fp["id_clase_tipo__nombre"] == "ini"]
    fin=fp[fp["id_clase_tipo__nombre"] == "fin"]
    print(dias_limite,inicio,fin)
    messages.info(request,"Captura realizada.")
    if request.method == 'POST':
        print("x")
    else:
        print("y")
    return agenda_profesores(request)
    #model = Agenda_Practica
    #template_name="agenda_practica_form.html"
    #success_url = reverse_lazy('PagGestion:agenda_profesores')
    #fields = ['id_laboratorio_horario','id_practica','fecha']

    #agregar dos registros por cada práctica
def instrucciones(request):
    messages.success(request,"Instrucciones de carga.")
    return render(request,'instrucciones_carga.html')
