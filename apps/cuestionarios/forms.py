from django import forms
from .models import Encuesta_Profesor
from django.utils.translation import ugettext_lazy as _
class PracticaForm(forms.ModelForm):

	class Meta : 
		model = Encuesta_Profesor
		fields = '__all__'
		labels={
		"folio":_("Folio"),
		"id_laboratorio_horario":"Laboratorio", 
		"id_profesor":"Alumno",
		"id_practica":"Número de práctica",
		"observaciones":"Observaciones",
		}
		help_texts = {'folio': _('Some useful help text.'),}
		error_messages = {'folio': {'max_length': _("This writer's name is too long."),
		},
			}
		widgets={
			'folio': forms.TextInput(attrs={'class':'form-control mr-auto ml-auto' ,'placeholder':'Folio' }),
            'id_laboratorio_horario':forms.Select(attrs={'class':'form-control'}),
            'id_profesor': forms.Select(attrs={'class':'form-control'}),
            'id_practica': forms.Select(attrs={'class':'form-control'}),
            'observaciones':forms.Textarea(attrs={'class':'form-control'}),
		}
		


class EncuestaProfesor(forms.ModelForm):
	class Meta :
		pass
		fields =[

		]