from django.contrib import admin
from .models import RespuestaProfesor
from django.apps import apps

class RespuestaModelAdmin(admin.ModelAdmin):
    list_display = [
    	"encuesta_id","servicio","cumplio_objetivo",
    	"apertura_oportuna","apertura_porque","id_laboratorista",
    	"permanencia_enpractica","permanencia_porque","colaboracion_practica",
    	"colaboracion_porque","entrega_equipo","entrega_porque"
    	]
    list_display_links = ["servicio","cumplio_objetivo"]
    list_filter = ["servicio","cumplio_objetivo"]
    search_fields = ["servicio","cumplio_objetivo"]
    #list_editable = ["titulo"]
    class Meta:
        model=RespuestaProfesor

admin.site.register(RespuestaProfesor,RespuestaModelAdmin)

app=apps.get_app_config('cuestionarios')
# Register your models here.
for model_name,model in app.models.items():
	#print(model_name)
	if model_name != "respuestaprofesor":
		admin.site.register(model)