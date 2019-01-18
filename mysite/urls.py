"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings


# from mysite.views import hola,fecha_actual,encuesta_profesores,encuesta_alumnos,asignacion
from .views import index

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sgc/',include('PagGestion.urls',namespace="PagGestion")),
    url(r'^$', index,name="home"),
    #url(r'^chaining/', include('smart_selects.urls')),
    url(r'^cuestionarios/', include('apps.cuestionarios.urls',namespace="cuestion",app_name="cuestionarios")),
    #url(r'^pract/', include('apps.cuestionarios.urls',namespace="pract",app_name="cuestionarios")),
    url(r'^index/', index, name='index'),
]
