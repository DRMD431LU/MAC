from django.conf.urls import url,include
from .views import cuestionario_laboratorio,cuestionario_practica,CuestionarioCreate

urlpatterns = [
		url(r'laboratorio',cuestionario_laboratorio,name="cuestionario_laboratorio"),
		url(r'practica',CuestionarioCreate.as_view(),name="cuestionario_practica"),
		

]	