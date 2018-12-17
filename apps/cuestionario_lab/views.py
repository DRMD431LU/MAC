from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request,"cuestionario_pract/cuestionario_practica.html",{})