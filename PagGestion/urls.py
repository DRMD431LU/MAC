from __future__ import unicode_literals

from django.conf.urls import url

from . import views

from .ajax import get_materia,get_profesor,get_grupo,get_practica,agendar_practica,get_laboratorio,get_horas,get_horaFin,obtener_practica,reagendar_practica,obtener_bloqueados,obtener_inicioFin
from .cargaPracticaExcel import agendar_practica_excel

urlpatterns = [
    url(r'^importar_Profesores/$',views.profesores_upload,name='importar_no_usar'),
    url(r'^importar_Horarios_Profesores/$',views.horarios_profesores_upload,name='importar_Profesores'),
    url(r'^importar_Horarios_Alumnos/$',views.cargar_alumnos,name='importar_horarios'),
    url(r'^acciones/$',views.acciones,name='acciones'),
    url(r'^agenda_profesores/$',views.agenda_profesores,name='agenda_profesores'),
    url(r'^generar_agenda/$',views.generar_agenda,name='generar_agenda'),
    url(r'^encuesta_laboratorio/$',views.encuesta_laboratorio,name='encuesta_laboratorio'),
    url(r'^encuesta_practica/$',views.encuesta_practica,name='encuesta_practica'),
    url(r'^ajax/get_materia/$', get_materia, name='get_materia'),
    url(r'^ajax/get_profesor/$', get_profesor, name='get_profesor'),
    url(r'^ajax/get_grupo/$', get_grupo, name='get_grupo'),
    url(r'^ajax/get_practica/$', get_practica, name='get_practica'),
    url(r'^ajax/agendar_practica/$', agendar_practica, name='agendar_practica'),
    url(r'^ajax/agendar_practica_excel/$', agendar_practica_excel, name='agendar_practica_excel'),
    url(r'^ajax/get_laboratorio/$', get_laboratorio, name='get_laboratorio'),
    url(r'^ajax/get_horas/$', get_horas, name='get_horas'),
    url(r'^ajax/get_horaFin/$', get_horaFin, name='get_horaFin'),
    url(r'^ajax/obtener_practica/$', obtener_practica, name='obtener_practica'),
    url(r'^ajax/reagendar_practica/$', reagendar_practica, name='reagendar_practica'),
    url(r'^ajax/obtener_bloqueados/$', obtener_bloqueados, name='obtener_bloqueados'),
    url(r'^ajax/obtener_inicioFin/$', obtener_inicioFin, name='obtener_inicioFin'),
    url(r'^instrucciones/$', views.instrucciones, name='instrucciones'),
]
