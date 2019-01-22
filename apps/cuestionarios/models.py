from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from datetime import datetime

#from smart_selects.db_fields import ChainedForeignKey

''' here goes my own data model'''

class Generacion(models.Model):
	valor=models.IntegerField(verbose_name="Generación")
	def __str__(self):
		return str(self.valor)


class Turno(models.Model):
	clave=models.IntegerField(primary_key=True)
	valor = models.CharField(max_length=100,verbose_name="Turno")
	def __str__(self):
		return self.valor


class Periodo(models.Model):
	nombre=models.CharField(max_length=15,primary_key=True)
	activo=models.BooleanField(default=False)
	def __str__(self):
		return self.nombre+"-"+str(self.activo)


class Carrera(models.Model):
	clave = models.CharField(max_length=100)
	Nombre = models.CharField(max_length=100)
	def __str__(self):
		return self.Nombre


class Grupos_Carrera(models.Model):
    clave=models.CharField(max_length=20, primary_key=True)
    id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
    id_turno=models.ForeignKey(Turno, on_delete=models.CASCADE,verbose_name="Turno")
    def __str__(self):
        return self.clave+"-"+self.id_carrera.Nombre


class Materia_Laboratorio(models.Model):
	clave = models.CharField(max_length=100, primary_key=True)
	nombre = models.CharField(max_length=100)
	id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
	def __str__(self):
		return self.nombre

class Alumno(models.Model):
    num_cuenta = models.CharField(max_length=20,primary_key=True)
    nombre = models.CharField(max_length=200)
    fecha_nac=models.DateField()
    email=models.EmailField(max_length=50,default="example@email.com")
    id_generacion = models.ForeignKey(Generacion, on_delete=models.CASCADE,verbose_name="Generación")
    id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
	#agregar teléfono pero no será editable
    def __str__(self):
        return self.nombre

class Profesor(models.Model):
	rfc = models.CharField(max_length=20, primary_key=True)
	nombre = models.CharField(max_length=200)
	num_empleado = models.IntegerField(verbose_name="Número de Empleado")
	id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
	correo_e = models.EmailField(max_length=200,verbose_name="Correo Electrónico")
	telefono_casa=models.CharField(max_length=14)
	telefono_oficina=models.CharField(max_length=14)
	created_at=models.DateTimeField(default=datetime.now,blank=True,verbose_name="Creado el")

	#telefono casa, oficina

	class Meta:
		verbose_name="Profesor"
		verbose_name_plural="Profesores"

	def __str__(self):
		return self.nombre

class Laboratorista(models.Model):
	nombre = models.CharField(max_length=100)
	rfc = models.CharField(max_length=20)
	num_empleado = models.IntegerField()
	correo_e = models.CharField(max_length=200)
	telefono_casa=models.CharField(max_length=14)
	telefono_oficina=models.CharField(max_length=14)
	id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
	created_at=models.DateTimeField(default=datetime.now,blank=True,verbose_name="Creado el")

	class Meta:
		verbose_name="Laboratorista"
		verbose_name_plural="Laboratoristas"

	def __str__(self):
		return self.nombre

class Laboratorio_Horario(models.Model):
	rfc = models.ForeignKey(Profesor, on_delete=models.CASCADE,verbose_name="Profesor")
	id_grupo=models.ForeignKey(Grupos_Carrera,on_delete=models.CASCADE,verbose_name="Grupo")
	id_clave_mat_lab=models.ForeignKey(Materia_Laboratorio, on_delete=models.CASCADE,verbose_name="Clave Materia")
	periodo=models.ForeignKey(Periodo,on_delete=models.CASCADE,verbose_name="Periodo")
	def __str__(self):
		return self.id_clave_mat_lab.nombre+"-"+self.rfc.nombre+"-"+str(self.id_grupo)

class Encuesta_Alumno(models.Model):
	folio = models.CharField(max_length=100, primary_key=True)
	id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE,null=True,blank=True)
	id_laboratorio_horario=models.ForeignKey(Laboratorio_Horario,on_delete=models.CASCADE,null=True,blank=True)
	created_at=models.DateTimeField(auto_now_add=True)
	observaciones=models.CharField(max_length=500,null=True,blank=True)


class Practica(models.Model):
	numero = models.IntegerField()
	nombre = models.CharField(max_length=100)
	materia_laboratorio=models.ForeignKey(Materia_Laboratorio,on_delete=models.CASCADE,verbose_name="Materia Laboratorio")
	predecesora=models.ForeignKey('self',on_delete=models.CASCADE,verbose_name="Práctica Predecesora",blank=True,null=True)
	class Meta:
		verbose_name="Práctica"
		verbose_name_plural="Prácticas"
	def __str__(self):
		return self.materia_laboratorio.nombre+"-"+"#"+str(self.numero)+" "+self.nombre


class EncuestaNombre(models.Model): #Evaluation scheme
	valor=models.CharField(max_length=30)
	def __str__(self):
		return self.valor

class EncuestaProfesor(models.Model): #evaluation
	folio = models.CharField(max_length=100, primary_key=True)
	id_laboratorio_horario = models.ForeignKey(Laboratorio_Horario, on_delete=models.CASCADE)
	id_profesor=models.ForeignKey(Profesor, on_delete=models.CASCADE)
	id_practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	observaciones=models.CharField(max_length=500)
	cuestionario = models.ForeignKey(EncuestaNombre)
	def __str__(self):
		return self.folio

class EncuestaPregunta(models.Model): #evaluation question
	reactivo=models.CharField(max_length=300)
	cuestionario=models.ForeignKey(EncuestaNombre)
	def __str__(self):
		return self.reactivo

class EncuestaRespuesta(models.Model): #evaluation answer
	encuesta = models.ForeignKey(EncuestaProfesor)
	reactivo = models.ForeignKey(EncuestaPregunta)
	respuesta = models.CharField(max_length=150)
	def __str__(self):
		return self.respuesta
RATING_CHOICES = ((0, u"Good"), (1, u"Bad"), (2, u"Dunno"),)

class EvaluationScheme(models.Model):
    title = models.CharField(max_length=200)

class Evaluation(models.Model):
    doctor = models.CharField(max_length=200)
    agency = models.CharField(max_length=200)
    scheme = models.ForeignKey(EvaluationScheme)

class EvaluationQuestion(models.Model):
    question = models.CharField(max_length=200)
    evaluation = models.ForeignKey(EvaluationScheme)

    def __unicode__(self):
        return self.question

class EvaluationAnswer(models.Model):
    evaluation = models.ForeignKey(Evaluation)
    question = models.ForeignKey(EvaluationQuestion)
    answer = models.SmallIntegerField(choices=RATING_CHOICES)

'''






































































class Horario(models.Model):
	hora=models.TimeField()
	def __str__(self):
		return str(self.hora)

class Dias(models.Model):
	dias=models.CharField(max_length=20,verbose_name="Día")
	class Meta:
		verbose_name = 'Día'
		verbose_name_plural = 'Días'
	def __str__(self):
		return str(self.dias)



class Plan(models.Model):
    nombre=models.CharField(max_length=200,verbose_name="Plan")
    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'








#perfil de Laboratorista, Jefe de Sección, Secretario técnico, Administrador. mismo perfil que profesor.
#para jefe de Sección agregar materias que pertenecen al jefe de sección y laboratorios como espacio físico que pertenecen a el.

class Laboratorio(models.Model):
	nombre = models.CharField(max_length=200)
	aula=models.CharField(max_length=10)
	carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
	def __str__(self):
		return self.nombre+"-"+self.aula

class Administrador(models.Model):
	nombre = models.CharField(max_length=100)
	rfc = models.CharField(max_length=20)
	num_empleado = models.IntegerField()
	correo_e = models.CharField(max_length=200)
	telefono_casa=models.CharField(max_length=14)
	telefono_oficina=models.CharField(max_length=14)
	created_at=models.DateTimeField(default=datetime.now,blank=True,verbose_name="Creado el")

	class Meta:
		verbose_name="Administrador"
		verbose_name_plural="Administradores"

	def __str__(self):
		return self.nombre


class SecretarioTecnico(models.Model):
	nombre = models.CharField(max_length=100)
	rfc = models.CharField(max_length=20)
	num_empleado = models.IntegerField()
	correo_e = models.CharField(max_length=200)
	telefono_casa=models.CharField(max_length=14)
	telefono_oficina=models.CharField(max_length=14)
	id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
	created_at=models.DateTimeField(default=datetime.now,blank=True,verbose_name="Creado el")

	class Meta:
		verbose_name="Secretario Técnico"
		verbose_name_plural="Secretarios Técnico"

	def __str__(self):
		return self.nombre

class JefeSeccion(models.Model):
	nombre = models.CharField(max_length=100)
	rfc = models.CharField(max_length=20)
	num_empleado = models.IntegerField()
	nombre_seccion = models.CharField(max_length=200)
	correo_e = models.CharField(max_length=200)
	telefono_casa=models.CharField(max_length=14)
	telefono_oficina=models.CharField(max_length=14)
	id_carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE,verbose_name="Carrera")
	created_at=models.DateTimeField(default=datetime.now,blank=True,verbose_name="Creado el")

	class Meta:
		verbose_name="Jefe de Sección"
		verbose_name_plural="Jefes de Sección"

	def __str__(self):
		return self.nombre

class Jefe_Laboratorios(models.Model):
	id_jefe = models.ForeignKey(JefeSeccion, on_delete=models.CASCADE,verbose_name="Jefe de Sección")
	id_laboratorio=models.ForeignKey(Laboratorio, on_delete=models.CASCADE,verbose_name="Laboratorio")





class Jefe_Materias(models.Model):
	id_jefe= models.ForeignKey(JefeSeccion, on_delete=models.CASCADE,verbose_name="Jefe de Sección")
	id_materia= models.ForeignKey(Materia_Laboratorio, on_delete=models.CASCADE,verbose_name="Materia Laboratorio")






class Horarios_Clase(models.Model):
	laboratorio_horario=models.ForeignKey(Laboratorio_Horario,on_delete=models.CASCADE,verbose_name="Horario Laboratorio")
	id_dias=models.ForeignKey(Dias,on_delete=models.CASCADE,verbose_name="Día")
	hora_ini=models.ForeignKey(Horario, on_delete=models.CASCADE,verbose_name="Hora Inicio",related_name="hora_ini")
	hora_fin=models.ForeignKey(Horario, on_delete=models.CASCADE,verbose_name="Hora Fin",related_name="hora_fin")


class Alumno_Inscrito(models.Model):
    id_alumno=models.ForeignKey(Alumno, on_delete=models.CASCADE,verbose_name="Alumno")
    id_laboratorio_horario = models.ForeignKey(Laboratorio_Horario, on_delete=models.CASCADE,verbose_name="Horario Laboratorio")
    def __str__(self):
        return self.id_alumno.nombre+"-"+str(self.id_laboratorio_horario)






class Respuesta_Profesor(models.Model):
	id_Encuesta_Profesor=models.ForeignKey(Encuesta_Profesor, on_delete=models.CASCADE)
	id_pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	valor=models.CharField(max_length=20)
	porque=models.CharField(max_length=500)





class Formato(models.Model):
    clave_formato = models.CharField(max_length=100)
    nombre_formato = models.CharField(max_length=100)
    rol_usuario = models.IntegerField()

class Aviso(models.Model):
	texto_aviso = models.CharField(max_length=100)
	prioridad = models.IntegerField()
	inicio_aviso = models.DateTimeField(max_length=100)
	fin_aviso = models.DateTimeField(max_length=100)
	rol_usuario=models.IntegerField()

class Tipo_Limite(models.Model):
	OPCIONES_NOMBRE=(("E_A","Encuesta Alumno"),
	("E_P","Encuesta Profesor"),
	("R_P","Reagendar_Practica"))
	nombre=models.CharField(max_length=3,choices=OPCIONES_NOMBRE,default="Enc_Alumno",unique=True)
	def __str__(self):
		return self.get_nombre_display()

class Clase_Tipo(models.Model):
	OPCIONES_NOMBRE=(("ini","Inicio"),
	("fin","Fin"))
	nombre=models.CharField(max_length=3,choices=OPCIONES_NOMBRE,default="ini",unique=True)
	def __str__(self):
		return self.get_nombre_display()

class Fecha_Limite(models.Model):
	fecha=models.DateTimeField()
	id_clase_tipo=models.ForeignKey(Clase_Tipo,on_delete=models.CASCADE,verbose_name="Tipo de Límite")
	id_tipo=models.ForeignKey(Tipo_Limite,on_delete=models.CASCADE,verbose_name="Límite para")
	class Meta:
		verbose_name="Fecha Límite"
		verbose_name="Fechas Límite"
	def __str__(self):
		return self.id_tipo.get_nombre_display()+"-"+self.id_clase_tipo.get_nombre_display()+"-"+str(self.fecha)

class Dia_No_Laborable(models.Model):
	fecha=models.DateField()

class Agenda_Practica(models.Model):
	laboratorio_horario=models.ForeignKey(Laboratorio_Horario, on_delete=models.CASCADE,verbose_name="Laboratorio Horario")
	practica=models.ForeignKey(Practica, on_delete=models.CASCADE,verbose_name="Práctica")
	fecha=models.DateTimeField(default=datetime.now, blank=True)
	hora_ini=models.TimeField(blank=True,default=datetime.now)
	hora_fin=models.TimeField(blank=True,default=datetime.now)
	reagendamiento=models.IntegerField(default=0)
	laboratorio=models.ForeignKey(Laboratorio, on_delete=models.CASCADE,verbose_name="Laboratorio")
	rfc = models.ForeignKey(Profesor, on_delete=models.CASCADE,verbose_name="Profesor")



	#24/03/2018
	#variable para realizar el conteo de reagendamientos.
	#variable para guardar quien activo las encuesta.

	#mostrar valores del perfil de cada uno
	#posibilidad de elegir perfil-Jonh

	#si trae observaciones, quejas y Sugerencias, agregar semaforo para cada una de ellos. validar textos básicos.
	#ocultar estos mismos a menos que se de clic, 250 carácteres
	#checar ediciones de menú
	#diego

	#funcionalidades. de agendamiento- mike
	#reprogramación validar espacio físico,  y fechas
	#checar que la práctica se reacomode sin pegarle a las consecutivas o moviendo todas las prácticas
	# agregar habilitación de 3 días para encuesta de profesores, a partir de la hora de fin

#junta el 14 de julio, 4 de agosto y 18 de agosto.

# Create your models here.
'''