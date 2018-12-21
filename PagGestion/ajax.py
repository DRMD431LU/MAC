from django.http import JsonResponse
import datetime

from .models import Carrera,Materia_Laboratorio,Profesor,Laboratorio_Horario,Practica,Agenda_Practica,Laboratorio,Dia_No_Laborable,Fecha_Limite
from django.db.models import Q
from django.db.models import F

def get_materia(request):
    carrera_id = request.GET.get('id_carrera')
    if carrera_id:
        materias = Materia_Laboratorio.objects.filter(id_carrera=carrera_id)
    else:
        materias = Materia_Laboratorio.objects.none()

    options = '<option value="" selected="selected">(Selecciona una Materia)</option>'

    for materia in materias:
        options += '<option value="%s">%s</option>' % (
            materia.pk,
            materia
        )
    response = {}
    response['materias'] = options
    return JsonResponse(response)

def get_profesor(request):
    carrera_id = request.GET.get('id_carrera')
    materia_id = request.GET.get('id_materia')
    if carrera_id and materia_id:
        profesores = Profesor.objects.filter(laboratorio_horario__id_grupo__id_carrera=carrera_id).filter(laboratorio_horario__id_clave_mat_lab__clave=materia_id).distinct()
    else:
        profesores = Profesor.objects.none()

    options = '<option value="" selected="selected">(Selecciona un Profesor)</option>'

    for profesor in profesores:
        options += '<option value="%s">%s</option>' % (
            profesor.rfc,
            profesor.nombre
        )
    response = {}
    response['profesores'] = options
    return JsonResponse(response)

def get_grupo(request):
    carrera_id = request.GET.get('id_carrera')
    materia_id = request.GET.get('id_materia')
    profesor_id= request.GET.get('id_profesor')
    todos=int(request.GET.get('todos'))
    #print(todos,not todos)
    if carrera_id and materia_id and profesor_id:
        grupos = Laboratorio_Horario.objects.filter(id_grupo__id_carrera=carrera_id).filter(id_clave_mat_lab__clave=materia_id)
        if not todos:
            grupos=grupos.filter(rfc=profesor_id)
    else:
        grupos = Laboratorio_Horario.objects.none()

    options = '<option value="" selected="selected">(Selecciona un Grupo)</option>'

    for grupo in grupos:
        options += '<option value="%s">%s</option>' % (
            grupo.pk,
            grupo.id_grupo.clave
        )
    response = {}
    response['grupos'] = options
    return JsonResponse(response)



def get_practica(request):
    carrera_id = request.GET.get('id_carrera')
    materia_id = request.GET.get('id_materia')
    profesor_id= request.GET.get('id_profesor')
    grupo_id= request.GET.get('id_grupo')
    if carrera_id and materia_id and profesor_id and grupo_id:
        practicas = Practica.objects.filter(materia_laboratorio__id_carrera=carrera_id).filter(materia_laboratorio__clave=materia_id)
    else:
        practicas = Practica.objects.none()

    options = '<option value="" selected="selected">(Selecciona una Práctica)</option>'

    for practica in practicas:
        options += '<option value="%s">%s</option>' % (
            practica.pk,
            practica.nombre
        )
    response = {}
    response['practicas'] = options
    return JsonResponse(response)

def time_plus(time,timedelta):
    start=datetime.datetime(2000,1,1,
            hour=time.hour,minute=time.minute,second=time.second)
    end=start+timedelta
    return end.time()

def obtener_hora(hora,minutos):
    x=list(map(int,hora.split(":")))
    un_minuto=datetime.timedelta(minutes=minutos)
    h1=time_plus(datetime.time(x[0],x[1]),un_minuto)
    return h1

def agendar_practica(request):
    response={}
    codigo=404
    if request.method=="POST":
        grupo=request.POST.get("grupo")
        fecha=datetime.datetime.strptime(request.POST.get("fecha_practica"), "%Y-%m-%d").date()
        profesor=request.POST.get("profesor")
        practica=request.POST.get("practica")
        hora_fin=request.POST.get("hora_fin")
        hora_ini=request.POST.get("hora_ini")
        laboratorio=request.POST.get("laboratorio")
            #validación para práctica ya existente
        agendadas=Agenda_Practica.objects.filter(
            laboratorio_horario_id=grupo,
            practica_id=practica)
        if agendadas.count()>0:
            response={"error":"Práctica ya agendada"}
            codigo=404
        else:
            #validación para laboratorio libre
            hi=obtener_hora(hora_ini,1)
            hf=obtener_hora(hora_fin,-1)
            last=Agenda_Practica.objects.filter(
                    Q(Q(hora_ini__range=(hi,hf))|
                    Q(hora_fin__range=(hi,hf)))|
                    Q(Q(hora_ini=hora_ini),
                    Q(hora_fin=hora_fin)),
                    laboratorio_id=laboratorio,
                    fecha=fecha
                )
            if last.count()>0:
                response={"error":"Laboratorio Ocupado"}
                codigo=404
            else:
            #validación para predecesora, validar si existe y esta agendada y si lo esta que sea para una fecha anterior a la que se intenta
                #valida si tiene predecesora
                practicaActual=Practica.objects.filter(pk=practica)[0]
                if practicaActual.predecesora!=None:
                    #se valida si exite predecesora.
                    ppredecesora=Agenda_Practica.objects.filter(
                            laboratorio_horario_id=grupo,
                            practica_id=practicaActual.predecesora
                        )
                    if ppredecesora.count()>0:
                        filtroP=ppredecesora.filter(
                            Q(Q(Q(hora_ini__gt=hi)|
                            Q(hora_fin__gt=hf))|
                            Q(Q(hora_ini=hora_ini),
                            Q(hora_fin=hora_fin)),
                            Q(fecha=fecha))|
                            Q(fecha__gt=fecha),
                        )
                        #se valida fecha de la predecesora
                        if filtroP.count()>0:
                            response={"error":"La práctica predecesora debe realizarce antes."}
                            codigo=404
                        else:
                                agenda,created=Agenda_Practica.objects.get_or_create(
                                        laboratorio_horario_id=grupo,
                                        practica_id=practica,
                                        fecha=fecha,
                                        rfc_id=profesor,
                                        laboratorio_id=laboratorio,
                                        hora_ini=hora_ini,
                                        hora_fin=hora_fin
                                )
                                if created:
                                    #agenda.reagendamiento=agenda.reagendamiento+1
                                    response={"mensaje":"ok"}
                                    codigo=200
                                else:
                                    response={"error":"Práctica ya existente"}
                                    codigo=404
                    else:
                        response={"error":"Predecesora no agendada"}
                        codigo=404
                else:
                    agenda,created=Agenda_Practica.objects.get_or_create(
                                laboratorio_horario_id=grupo,
                                practica_id=practica,
                                rfc_id=profesor,
                                fecha=fecha,
                                laboratorio_id=laboratorio,
                                hora_ini=hora_ini,
                                hora_fin=hora_fin
                            )
                    if created:
                        #agenda.reagendamiento=agenda.reagendamiento+1
                        response={"mensaje":"ok"}
                        codigo=200
                    else:
                        response={"error":"Práctica ya existente"}
                        codigo=404
    return JsonResponse(response,status=codigo)

def get_laboratorio(request):
    carrera_id = request.GET.get('id_carrera_laboratorio')
    if carrera_id:
        laboratorios = Laboratorio.objects.filter(carrera=carrera_id)
    else:
        laboratorios = Laboratorio.objects.none()

    options = '<option value="" selected="selected">(Selecciona el aula del laboratorio)</option>'

    for laboratorio in laboratorios:
        options += '<option value="%s">%s</option>' % (
            laboratorio.pk,
            laboratorio
        )
    response = {}
    response['laboratorios'] = options
    return JsonResponse(response)

def get_horas(request):
    response={}
    fecha=request.GET.get("fecha")
    #print(fecha)
    options = '<option value="" selected="selected">(Selecciona la Hora de Inicio de la Práctica)</option>'
    if 1:
        for x in range(7,22,1):
            for y in range(0,59,5):
                options += '<option value="%s">%s</option>' % (
                    (str(x) if x>=10 else "0"+str(x))+":"+(str(y) if y>=10 else "0"+str(y)),
                    (str(x) if x>=10 else "0"+str(x))+":"+(str(y) if y>=10 else "0"+str(y))
                )
        response['horas']=options
        codigo=200
    else:
        response={"error":"No hay Horarios Disponibles"}
        codigo=404
    #response = {}
    #response['valor'] = "valor"
    return JsonResponse(response,status=codigo)


def get_horaFin(request):
    response={}
    horaIni=request.GET.get("id_hora_ini")
    fecha=datetime.datetime.strptime(request.GET.get("id_fecha_practica"), "%Y-%m-%d").date()
    #print(fecha)
    hora,minutos=horaIni.split(":")
    #x=[(i, datetime.time(i).strftime('%H:%M')) for i in range(24)]
    #select * from aulas where fecha = '2016-05-17' and (horainicio <= '18:30' and horafin >= '18:30' or horainicio <= '19:30' and horafin >= '19:30' or horainicio > '18:30' and horafin < '19:30');
    options = '<option value="" selected="selected">(Selecciona la Hora de Fin de la Práctica)</option>'
    if 1:
        for x in range(7,22,1):
            if(x>=int(hora)):
                for y in range(0,59,5):
                    if((x>=int(hora) and y>=int(minutos)+30) or (x>int(hora)) and not (x==int(hora)+1 and int(minutos)-30>y)):
                        options += '<option value="%s">%s</option>' % (
                            (str(x) if x>=10 else "0"+str(x))+":"+(str(y) if y>=10 else "0"+str(y)),
                            (str(x) if x>=10 else "0"+str(x))+":"+(str(y) if y>=10 else "0"+str(y))
                        )
        response['horasFin']=options
        codigo=200
    else:
        response={"error":"No hay Horarios Disponibles"}
        codigo=404
    #response = {}
    #response['valor'] = "valor"
    return JsonResponse(response,status=codigo)

def obtener_practica(request):
    id=request.GET.get("id")
    agenda=Agenda_Practica.objects.get(id=id)
    response={"carrera":agenda.laboratorio_horario.id_grupo.id_carrera.id,
              "materia":agenda.laboratorio_horario.id_clave_mat_lab.pk,
              "profesor":agenda.rfc.rfc,
              "grupo":agenda.laboratorio_horario.pk,
              "practica":agenda.practica.id,
              "carrera_laboratorio":agenda.laboratorio.carrera.pk,
              "laboratorio":agenda.laboratorio.pk,
              "fecha":agenda.fecha.strftime("%Y-%m-%d"),
              "hora_ini":agenda.hora_ini.strftime("%H:%M"),
              "hora_fin":agenda.hora_fin.strftime("%H:%M"),
    }

    return JsonResponse(response)

def reagendar_practica(request):
    #falta validar que la actual no tenga sucesora y si la obtiene
    #hay que validar que se realice antes que la posterior
    response={}
    codigo=404
    if request.method=="POST":
        #obtenemos las variables enviadas en el formulario
        grupo=request.POST.get("grupo")
        practica=request.POST.get("practica")
        fecha=datetime.datetime.strptime(request.POST.get("fecha_practica"), "%Y-%m-%d").date()
        hora_fin=request.POST.get("hora_fin")
        hora_ini=request.POST.get("hora_ini")
        laboratorio=request.POST.get("laboratorio")
        id_edicion=request.POST.get("pk")
        profesor=request.POST.get("profesor")

        #variables extra para realizar el reagendamiento
        fecha_ultima=request.POST.get("fecha_practica_final")
        hora_ini_ultima=request.POST.get("hora_ini_final")
        hora_fin_ultima=request.POST.get("hora_fin_final")

        #validar que onda con el agregar fecha de reagendamiento
        agendadas=Agenda_Practica.objects.filter(
                    fecha=fecha,
                    hora_ini=hora_ini,
                    hora_fin=hora_fin,
                    rfc_id=profesor,
                    laboratorio_horario_id=grupo,
                    practica_id=practica,
                    laboratorio=laboratorio
                )
        if agendadas.count()>0:
            response={"error":"No se detectaron cambios."}
            codigo=404
        else:
            #validación para laboratorio libre
            #se limpian y optimizan las variables de hora
            #sumando o restando un minuto
            hi=obtener_hora(hora_ini,1)
            hf=obtener_hora(hora_fin,-1)
            #consulta a Base de Datos
            last=Agenda_Practica.objects.filter(
                    Q(Q(hora_ini__range=(hi,hf))|
                    Q(hora_fin__range=(hi,hf)))|
                    Q(Q(hora_ini=hora_ini),
                    Q(hora_fin=hora_fin)),
                    laboratorio_id=laboratorio,
                    fecha=fecha,
                ).exclude(
                Q(id=id_edicion)|
                Q(laboratorio_horario_id=grupo))
                # agregar el grupo para mostrar solo aquella
            #se valida que se obtengan resultados para indicar
            #que el laboratorio está ocupado.
            if last.count()>0:
                response={"error":"Laboratorio Ocupado"}
                codigo=404
                #workin'
            else:
                 if not validaPredecesora(request):
                     #se valida que el espacio no este siendo ocupado por el mismo grupo
                    mismoGrupo=Agenda_Practica.objects.filter(
                            Q(Q(hora_ini__range=(hi,hf))|
                            Q(hora_fin__range=(hi,hf)))|
                            Q(Q(hora_ini=hora_ini),
                            Q(hora_fin=hora_fin)),
                            fecha=fecha,
                            laboratorio_horario_id=grupo,
                    ).exclude(
                            id=id_edicion
                    )
                    if mismoGrupo.count()>0:
                        #validación para no permitir el reagendamiento de Prácticas
                        #que sean consecutivas no importa si es sucesora o antecesora

                            #validamos que se trate del primer intento de agendamiento.
                            #en caso de ser el segundo ya tenemos los datos del agendamiento
                            #de la última práctica
                            #falta someter a pruebas el código de validar última.
                        if(fecha_ultima is None and hora_fin_ultima is None and hora_ini_ultima is None):
                            datos=Agenda_Practica.objects.order_by("-fecha")[0]
                            #obtenemos la fecha más alta para que el calendario de reagendamiento.
                            #solo se muestre a partir de esa fecha
                            fecha_reagendamiento=datos.fecha.date() if datos.fecha.date()>fecha else fecha
                            #mensaje para mostar los campos extra y limitar el calendario.
                            response={"predecesora":"La práctica es antecesora de otra, por lo que se recorreran las prácticas.",
                                        "fecha":fecha_reagendamiento.strftime("%Y-%m-%d")}
                            #codigo de error
                            codigo=404
                        else:
                            #mensaje para mostar los campos extra y limitar el calendario.
                            if validaFinal(request):
                                datos=Agenda_Practica.objects.order_by("-fecha")[0]
                                #obtenemos la fecha más alta para que el calendario de reagendamiento.
                                #solo se muestre a partir de esa fecha
                                fecha_reagendamiento=datos.fecha.date() if datos.fecha.date()>fecha else fecha
                                response={"error":"Laboratorio Ocupado para la última práctica.",
                                        "fecha":fecha_reagendamiento.strftime("%Y-%m-%d")}
                                codigo=404
                            else:
                                    mismoGrupo=mismoGrupo[0]
                                    #falta validar que no se empalmen los nuevos horarios y que haya disponibilidad para la fecha y hora final
                                    fecha_ultima=datetime.datetime.strptime(request.POST.get("fecha_practica_final"), "%Y-%m-%d").date()
                                    hif=obtener_hora(hora_ini_ultima,1)
                                    hff=obtener_hora(hora_ini_ultima,-1)
                                    #consulta a Base de Datos
                                    #obtenemos el agendamiento de la práctica que se editará
                                    estaPractica=Agenda_Practica.objects.get(pk=id_edicion)
                                    #obtenemos los datos de las prácticas que siguen a la práctica a editar
                                    reagendar=Agenda_Practica.objects.filter(
                                            Q(Q(Q(fecha=estaPractica.fecha),
                                            Q(hora_ini__gt=estaPractica.hora_ini),
                                            Q(hora_fin__gt=estaPractica.hora_fin))|
                                            Q(fecha__gt=estaPractica.fecha)),
                                            laboratorio_horario_id=grupo,
                                        ).order_by("fecha","hora_ini","hora_fin")
                                    #contador
                                    i=0
                                    #falta validar que las fechas ultimas no se empalmen con
                                    #última práctica
                                    #se recorren las prácticas faltantes.
                                    for practicaX in reagendar:

                                        if i != reagendar.count()-1 :
                                            siguiente=Agenda_Practica.objects.filter(
                                                    Q(Q(Q(fecha=practicaX.fecha),
                                                    Q(hora_ini__gt=practicaX.hora_ini),
                                                    Q(hora_fin__gt=practicaX.hora_fin))|
                                                    Q(fecha__gt=practicaX.fecha)),
                                                    laboratorio_horario_id=grupo,
                                                ).order_by("fecha","hora_ini","hora_fin")[0]

                                        if i==0:
                                            #se reagenda a la fecha proporcionada en la parte superior del formulario
                                            Agenda_Practica.objects.filter(pk=id_edicion).update(
                                                laboratorio_horario_id=grupo,
                                                rfc_id=profesor,
                                                practica_id=practica,
                                                laboratorio_id=laboratorio,
                                                fecha=fecha,
                                                hora_ini=hora_ini,
                                                hora_fin=hora_fin,
                                                reagendamiento=F("reagendamiento")+1
                                            )
                                            if not reagendar.count()==1:
                                                Agenda_Practica.objects.filter(pk=practicaX.id).update(
                                                    fecha=siguiente.fecha,
                                                    hora_ini=siguiente.hora_ini,
                                                    hora_fin=siguiente.hora_fin,
                                                    reagendamiento=siguiente.reagendamiento+1
                                                )
                                            else:
                                                Agenda_Practica.objects.filter(pk=practicaX.id).update(
                                                    fecha=fecha_ultima,
                                                    hora_ini=hora_ini_ultima,
                                                    hora_fin=hora_fin_ultima,
                                                    reagendamiento=F("reagendamiento")+1
                                                )
                                        elif i==reagendar.count()-1:
                                            #se reagenda la ultima práctica
                                            Agenda_Practica.objects.filter(pk=practicaX.id).update(
                                                fecha=fecha_ultima,
                                                hora_ini=hora_ini_ultima,
                                                hora_fin=hora_fin_ultima,
                                                reagendamiento=F("reagendamiento")+1
                                            )
                                        else:
                                            #se reagendan las intermedias
                                            #hay que validar este asunto sino
                                            #print(practicaX.pk,siguiente.query,siguiente.count())
                                            Agenda_Practica.objects.filter(pk=practicaX.id).update(
                                                fecha=siguiente.fecha,
                                                hora_ini=siguiente.hora_ini,
                                                hora_fin=siguiente.hora_fin,
                                                reagendamiento=siguiente.reagendamiento+1
                                            )
                                        i=i+1
                                        response={"mensaje":"Prácticas Reagendadas"}
                                        codigo=200

                    else:
                        Agenda_Practica.objects.filter(pk=id_edicion).update(
                            fecha=fecha,
                            rfc_id=profesor,
                            laboratorio_id=laboratorio,
                            hora_ini=hora_ini,
                            hora_fin=hora_fin
                        )
                        response={"mensaje":"Práctica Reagendada"}
                        codigo=200
                 else:
                    response={"error":"No se puede reagendar debido a la relación entre esta práctica y la siguiente."}
                    codigo=404

    return JsonResponse(response,status=codigo)

def validaFinal(request):
    valor=False
    grupo=request.POST.get("grupo")
    fecha_ultima=datetime.datetime.strptime(request.POST.get("fecha_practica_final"),"%Y-%m-%d").date()
    hora_ini_ultima=request.POST.get("hora_ini_final")
    hora_fin_ultima=request.POST.get("hora_fin_final")

    hi=obtener_hora(hora_ini_ultima,1)
    hf=obtener_hora(hora_fin_ultima,-1)
    #consulta a Base de Datos
    last=Agenda_Practica.objects.filter(
            laboratorio_horario_id=grupo
        ).order_by(
            "-fecha",
            "-hora_ini",
            "-hora_fin"
        )[0]
    print(last.id)
    ocupado=Agenda_Practica.objects.filter(
            Q(Q(hora_ini__range=(hi,hf))|
            Q(hora_fin__range=(hi,hf)))|
            Q(Q(hora_ini=hora_ini_ultima),
            Q(hora_fin=hora_fin_ultima)),
            fecha=fecha_ultima,
            laboratorio=last.laboratorio
        ).exclude(Q(laboratorio_horario_id=grupo))
        # agregar el grupo para mostrar solo aquella
    #se valida que se obtengan resultados para indicar
    #que el laboratorio está ocupado.
    if ocupado.count()>0:
        valor= True

    return valor

def validaPredecesora(request):
    #falta probar función y validar respuestas y carga
    valor = False
    grupo=request.POST.get("grupo")
    practica=request.POST.get("practica")
    fecha=datetime.datetime.strptime(request.POST.get("fecha_practica"), "%Y-%m-%d").date()
    hora_fin=request.POST.get("hora_fin")
    hora_ini=request.POST.get("hora_ini")
    laboratorio=request.POST.get("laboratorio")
    id_edicion=request.POST.get("pk")

    #formateamos las horas para realizar validaciones.
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
            #print(ppredecesora.count(),filtroP.count(),filtroP.query)
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
                #se valida que la predecesora se encuentre agendada después de la
                # fecha de la práctica actual
                #print(tienePredecesora,ppredecesora,filtroP)
                if filtroP.count()==0:
                    #mensaje para solicitar fecha de la última práctica
                    #y reagendar recorriendo las fechas
                    valor=True
            else:
                valor=True
    return valor

def obtener_bloqueados(request):

    dias=Dia_No_Laborable.objects.all()
    dias = dias.extra(select={'dias':"DATE_FORMAT(fecha, '%%d/%%m/%%Y')"})
    dias = dias.values_list("dias",flat=True)
    response={"dias":list(dias)}
    return JsonResponse(response)

def obtener_inicioFin(request):

    fechas=Fecha_Limite.objects.filter(id_tipo__nombre="R_P")
    ini=fechas.filter(id_clase_tipo__nombre="ini")[0].fecha.date().strftime("%Y-%m-%d")
    fin=fechas.filter(id_clase_tipo__nombre="fin")[0].fecha.date().strftime("%Y-%m-%d")
    response={"inicio":ini,
              "fin":fin}
    return JsonResponse(response)
##https://es.stackoverflow.com/questions/2040/select-dependiente-en-django

#select * from aulas where fecha = '2016-05-17'
#and (horainicio <= '18:30' and horafin >= '18:30'
#or horainicio <= '19:30' and horafin >= '19:30'
#or horainicio > '18:30' and horafin < '19:30');


#Para generar query quitando horas ocupadas,
#sería obtener todos los horarios
#que se encuentren dentro de un rango
#una vez obtenidos todos los rangos de horas ocupadas
# solicitar query obteniendo los que no se encuentren
# en la unión de los rangos ocupandos

#14 agosto
#agregar casilla para mostrar comentario y/o queja para diego

#
#agregar caso de otro profesor dando la materia y modulo de carga por csv, mientras realizar los agendamientos correctamente

#agregar tabla de relación que se crea entre la materia y el espacio físico



#si la práctica tiene predecesora se debe realizar inmediatamente
#validar para obtener la fecha de bloqueo en calendario.
#validar los reagendamientos inmediatos.
#validar el reagendiento a la misma misma fecha y hora de la siguiente práctica.
#validar fechas no laborables.
#mensaje para recordar lo del 28


#agregar contador de reagendamiento a la tabla
# pregunte si,reagendar prácticas del mismo grupo y misma hora
#el grupo ya no cambia, por lo que ya no se cambia.
#práctica ya no se mueve.
#materia no se mueve, carrera

#solo secretarío técnico y admin pueden agregar las prácticas
#agregar contador de reagendamiento


#Checar css
