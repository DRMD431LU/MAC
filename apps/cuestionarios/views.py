from django.shortcuts import render,render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from apps.cuestionarios.models import EncuestaProfesor
from .forms import PracticaForm

# Create your views here.


def cuestionario_laboratorio(request):
	return render(request,"cuestionarios/cuestionario_laboratorio.html",{})
# Create your views here.
def cuestionario_practica(request):
	return render(request,"cuestionarios/cuestionario_practica.html",{})

class CuestionarioCreate(CreateView):
	model=EncuestaProfesor
	template_name='cuestionarios/cuestionario_practica.html'
	form_class = PracticaForm
	#second_form_class = LaboratorioForm
	success_url=reverse_lazy('PagGestion:acciones')

	# def get_context_data(self,**kwargs):
	# 	context=super(CuestionarioCreate,self).get_context_data(**kwargs)
	# 	if 'form' not in context:
	# 		context['form'] = self.form_class(self.request.GET)
	# 	if 'form2' not in context:
	# 		context['form2'] = self.second_form_class(self.request.GET)
	# 	return context

	# def cuestionario(self,request,*args,**kwargs):
	# 	self.object= self.get_object
	# 	form = self.form_class(request.POST)
	# 	form2=self.second_form_class(request.POST)
	# 	if form.is_valid() and form2.is_valid():
	# 		cuestionario_practica = form.save(commit=False)
	# 		cuestionario_practica.persona=form2.save()
	# 		cuestionario_practica.save()
	# 		return HttpResponseRedirect(self.get_success_url())
	# 	else: 
	# 		return self.render_to_response(self.get_context_data(form=form,form2=form2))


