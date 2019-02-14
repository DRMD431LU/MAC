from django.shortcuts import render,render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from apps.cuestionarios.models import RespuestaProfesor,Agenda_Practica
from .forms import PreguntasForm

# Create your views here.


def cuestionario_laboratorio(request):
	return render(request,"cuestionarios/cuestionario_laboratorio.html",{})
# Create your views here.
def cuestionario_practica(request):
	return render(request,"cuestionarios/cuestionario_practica.html",{})

class CuestionarioCreate(CreateView):
	model = RespuestaProfesor
	template_name = 'cuestionarios/cuestionario_practica.html'
	form_class = PreguntasForm
	#second_form_class = PracticaForm
	success_url = reverse_lazy('PagGestion:acciones')

	def get_context_data(self,**kwargs):
		context=super(CuestionarioCreate,self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		return context