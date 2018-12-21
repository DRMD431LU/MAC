from __future__ import unicode_literals

from django.contrib import admin
from django.apps import apps

app=apps.get_app_config('PagGestion')

for model_name,model in app.models.items():
    admin.site.register(model)

# Register your models here.
#se agregan comenarios para cargar prueba
#más comentarios.
#comentarios rama agendamiento
