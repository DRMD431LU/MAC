from django import forms
from .models import Encuesta_Alumno

class LaboratorioForm(forms.ModelForm):
	class Meta : 
		model = Encuesta_Alumno
		fields = [
		"folio",
		"id_alumno",
		"id_laboratorio_horario", 
		# "observaciones",
		]
		widgets={
		
		}
		labesls={


		}

class GruposForm(forms.ModelForm):
	class Meta : 
		model = Encuesta_Alumno
		fields = [
		"folio",
		"id_alumno",
		"id_laboratorio_horario", 
		# "observaciones",
		]