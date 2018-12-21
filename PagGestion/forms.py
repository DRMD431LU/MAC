from django import forms
from .models import Agenda_Practica,Materia_Laboratorio,Carrera,Practica,Laboratorio_Horario,Profesor,Laboratorio
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class UploadForm(forms.Form):
    f=forms.FileField()


class Agenda_PracticaForm(forms.Form):
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), empty_label="(Selecciona una Carrera)",required=True)
    materia=forms.ModelChoiceField(queryset=Materia_Laboratorio.objects.none(), empty_label="(Selecciona una Materia)",required=True)
    profesor=forms.ModelChoiceField(queryset=Profesor.objects.none(), empty_label="(Selecciona un Profesor)",required=True)
    grupo=forms.ModelChoiceField(queryset=Laboratorio_Horario.objects.none(), empty_label="(Selecciona un Grupo)",required=True)
    practica=forms.ModelChoiceField(queryset=Practica.objects.none(), empty_label="(Selecciona una Práctica)",required=True)
    fecha_practica=forms.DateField(help_text="Selecciona la fecha para realizar la práctica",label="Fecha de Práctica",required=True, widget=forms.DateInput(attrs={'type':'date'}))
    hora_ini=forms.ChoiceField(choices=[("","(Selecciona la Hora de Inicio de la Práctica)"),],label="Hora de Inicio de Práctica", help_text="Hora de Inicio de Práctica")
    hora_fin=forms.ChoiceField(choices=[("","(Selecciona la Hora de Fin de la Práctica)"),],label="Hora de Fin de Práctica", help_text="Hora de Fin de Práctica")
    carrera_laboratorio=forms.ModelChoiceField(queryset=Carrera.objects.all(), empty_label="(Selecciona la carrera a la que pertenece el laboratorio)",required=True)
    laboratorio=forms.ModelChoiceField(queryset=Laboratorio.objects.none(), empty_label="(Selecciona el aula del laboratorio)",required=True)

    def clean_fecha_practica(self):
        data = self.cleaned_data['fecha_practica']

        if data < datetime.date.today():
            raise ValidationError(_('La fecha debe ser a futuro'))
        return data
