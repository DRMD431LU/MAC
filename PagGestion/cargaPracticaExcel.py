from django.http import JsonResponse

import datetime

from .models import Carrera,Materia_Laboratorio,Profesor,Laboratorio_Horario,Practica,Agenda_Practica,Laboratorio,Dia_No_Laborable,Fecha_Limite
from django.db.models import Q
from django.db.models import F
from .forms import UploadForm
from .ajax import obtener_hora
from django.shortcuts import get_object_or_404


def agendar_practica_excel(request):
    response={"error":"Archivo no Válido"}
    codigo=404
    if request.method=="POST":
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            c=0
            first=True
            nombre_carrera,archivo,valido=validarCarrera(request)
            if valido:
                lineas=archivo.split('\n')
                i=1
                mensajeCompleto=""
                for row in lineas:
                    if first is not True:
                        columnas=row.split(',')
                        if columnas[0] != '':
                            mensaje=crearPractica(columnas,encabezados)
                            if mensaje=="ok":
                                c+=1
                            else:
                                mensajeCompleto+="Error en la línea " + str(i) + " " + mensaje +"\n"
                        i+=1
                    else:
                        encabezados=row.split(',')
                        first=False
                if (c>0 or len(mensajeCompleto)>0) :
                    response={"c":c,"mensajeCompleto":mensajeCompleto}
                    codigo=200
    return JsonResponse(response,status=codigo)

def validarCarrera(request):
    valido=True
    s1=request.FILES['f'].name.replace('Prácticas.csv','').replace('_',' ').split()
    nombre_carrera=" ".join(s1)
    id_carrera=get_object_or_404(Carrera,Nombre=nombre_carrera)
    archivo=request.FILES['f'].read().decode('utf-8')

    return nombre_carrera,archivo,valido
#función para validar si el laboratorio se encuentra ocupado.
def validaOcupacion(hora_ini,hora_fin,fecha,aula,grupo):
    valor=False
    hi=obtener_hora(hora_ini,1)
    hf=obtener_hora(hora_fin,-1)
    ocupado=Agenda_Practica.objects.filter(
            Q(Q(hora_ini__range=(hi,hf))|
            Q(hora_fin__range=(hi,hf)))|
            Q(Q(hora_ini=hora_ini),
            Q(hora_fin=hora_fin)),
            fecha=fecha,
            laboratorio=aula
        )
        # agregar el grupo para mostrar solo aquella
    #se valida que se obtengan resultados para indicar
    #que el laboratorio está ocupado.
    if ocupado.count()>0:
        valor= True

    return valor

def validaPredecesora(hora_ini,hora_fin,fecha,grupo,practica,laboratorio):
    valor=False
    hi=obtener_hora(hora_ini,1)
    hf=obtener_hora(hora_fin,-1)
    esPredecesora=Practica.objects.filter(predecesora=practica)
    if esPredecesora.count()>0:
        ppredecesora=Agenda_Practica.objects.filter(
                laboratorio_horario_id=grupo,
                practica_id=esPredecesora[0].id
            )
            #validamos que se encuentre registrada la práctica
        if ppredecesora.count()>0:
            filtroP=Agenda_Practica.objects.filter(
                Q(laboratorio_horario_id=grupo),
                Q(Q(Q(hora_ini__gt=hi)|
                Q(hora_fin__gt=hf))|
                Q(Q(hora_ini=hora_ini),
                Q(hora_fin=hora_fin)),
                Q(fecha=fecha))|
                Q(fecha__gt=fecha),
                practica_id=esPredecesora[0].id
            )

            #mensaje para solicitar fecha de la última práctica
            #y reagendar recorriendo las fechas
            if filtroP.count() == 0:
                valor=True
        else:
            valor=True

    tienePredecesora=Practica.objects.filter(id=practica)
    if tienePredecesora.count()>0:
        if tienePredecesora[0].predecesora!=None:
            ppredecesora=Agenda_Practica.objects.filter(
                    laboratorio_horario_id=grupo,
                    practica_id=tienePredecesora[0].predecesora
                )

            #validamos que tengamos resultados
            if ppredecesora.count()>0:
                filtroP=ppredecesora.filter(
                    Q(Q(Q(hora_ini__lte=hi)|
                    Q(hora_fin__lte=hf))|
                    Q(Q(hora_ini=hora_ini),
                    Q(hora_fin=hora_fin)),
                    Q(fecha=fecha))|
                    Q(fecha__lt=fecha),
                    practica_id=tienePredecesora[0].predecesora
                )
                #se valida que la predecesora se encuentre agendada antes de la
                # fecha de la práctica actual

                if filtroP.count()==0:
                    #mensaje para solicitar fecha de la última práctica
                    #y reagendar recorriendo las fechas
                    valor=True
            else:
                valor=True
        
    return valor

def validaExistente(grupo,practica):
    valor=False
    agendadas=Agenda_Practica.objects.filter(
        laboratorio_horario_id=grupo,
        practica_id=practica)
    if agendadas.count()>0:
        valor=True
    return valor

def crearPractica(columnas,encabezados):
    valor=""

    carrera=columnas[0]
    laboratorio=columnas[1]
    profesor=columnas[2]
    grupo=columnas[3]
    practica=columnas[4]
    carrera_lab=columnas[5]
    aula=columnas[6]
    fecha=datetime.datetime.strptime(columnas[7], "%Y/%m/%d").date()
    hora_ini=columnas[8]
    hora_fin=columnas[9]

    practica=Practica.objects.get(numero=practica,materia_laboratorio_id=laboratorio).id
    aula=Laboratorio.objects.get(aula=aula,carrera__Nombre=carrera_lab).id
    grupo=Laboratorio_Horario.objects.get(id_grupo=grupo,id_clave_mat_lab=laboratorio).id

    existente=validaExistente(grupo,practica)
    ocupado=validaOcupacion(hora_ini,hora_fin,fecha,aula,grupo)
    predecesora=validaPredecesora(hora_ini,hora_fin,fecha,grupo,practica,laboratorio)

    if ((not existente) and (not ocupado) and (not predecesora)):
        agenda,created=Agenda_Practica.objects.get_or_create(
                laboratorio_horario_id=grupo,
                practica_id=practica,
                fecha=fecha,
                rfc_id=profesor,
                laboratorio_id=aula,
                hora_ini=hora_ini,
                hora_fin=hora_fin
        )
        if created:
            #se regresa true para contar la cantidad de horarios creados
            valor="ok"
    else:
        if existente:
            valor+="Práctica Ya Agendada. "
        if ocupado:
            valor+="Laboratorio Ocupado. "
        if predecesora:
            valor+="Predecesora No Agendada. "
    return valor
