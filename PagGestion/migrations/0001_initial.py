# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-21 15:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=20)),
                ('num_empleado', models.IntegerField()),
                ('correo_e', models.CharField(max_length=200)),
                ('telefono_casa', models.CharField(max_length=14)),
                ('telefono_oficina', models.CharField(max_length=14)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Creado el')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
        ),
        migrations.CreateModel(
            name='Agenda_Practica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('hora_ini', models.TimeField(blank=True, default=datetime.datetime.now)),
                ('hora_fin', models.TimeField(blank=True, default=datetime.datetime.now)),
                ('reagendamiento', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('num_cuenta', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('fecha_nac', models.DateField()),
                ('email', models.EmailField(default='example@email.com', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Alumno_Inscrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Alumno', verbose_name='Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Aviso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_aviso', models.CharField(max_length=100)),
                ('prioridad', models.IntegerField()),
                ('inicio_aviso', models.DateTimeField(max_length=100)),
                ('fin_aviso', models.DateTimeField(max_length=100)),
                ('rol_usuario', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=100)),
                ('Nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Clase_Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('ini', 'Inicio'), ('fin', 'Fin')], default='ini', max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dia_No_Laborable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Dias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dias', models.CharField(max_length=20, verbose_name='Día')),
            ],
            options={
                'verbose_name': 'Día',
                'verbose_name_plural': 'Días',
            },
        ),
        migrations.CreateModel(
            name='Encuesta_Alumno',
            fields=[
                ('folio', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.CharField(max_length=500)),
                ('id_alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta_Profesor',
            fields=[
                ('folio', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Fecha_Limite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('id_clase_tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Clase_Tipo', verbose_name='Tipo de Límite')),
            ],
            options={
                'verbose_name': 'Fechas Límite',
            },
        ),
        migrations.CreateModel(
            name='Formato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave_formato', models.CharField(max_length=100)),
                ('nombre_formato', models.CharField(max_length=100)),
                ('rol_usuario', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Generacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField(verbose_name='Generación')),
            ],
        ),
        migrations.CreateModel(
            name='Grupos_Carrera',
            fields=[
                ('clave', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('id_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Horarios_Clase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_fin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hora_fin', to='PagGestion.Horario', verbose_name='Hora Fin')),
                ('hora_ini', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hora_ini', to='PagGestion.Horario', verbose_name='Hora Inicio')),
                ('id_dias', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Dias', verbose_name='Día')),
            ],
        ),
        migrations.CreateModel(
            name='Jefe_Laboratorios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Jefe_Materias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='JefeSeccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=20)),
                ('num_empleado', models.IntegerField()),
                ('nombre_seccion', models.CharField(max_length=200)),
                ('correo_e', models.CharField(max_length=200)),
                ('telefono_casa', models.CharField(max_length=14)),
                ('telefono_oficina', models.CharField(max_length=14)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Creado el')),
                ('id_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera')),
            ],
            options={
                'verbose_name': 'Jefe de Sección',
                'verbose_name_plural': 'Jefes de Sección',
            },
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('aula', models.CharField(max_length=10)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Laboratorio_Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Laboratorista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=20)),
                ('num_empleado', models.IntegerField()),
                ('correo_e', models.CharField(max_length=200)),
                ('telefono_casa', models.CharField(max_length=14)),
                ('telefono_oficina', models.CharField(max_length=14)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Creado el')),
                ('id_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera')),
            ],
            options={
                'verbose_name': 'Laboratorista',
                'verbose_name_plural': 'Laboratoristas',
            },
        ),
        migrations.CreateModel(
            name='Materia_Laboratorio',
            fields=[
                ('clave', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('id_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('nombre', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('activo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Plan')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
            },
        ),
        migrations.CreateModel(
            name='Practica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('materia_laboratorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Materia_Laboratorio', verbose_name='Materia Laboratorio')),
                ('predecesora', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Practica', verbose_name='Práctica Predecesora')),
            ],
            options={
                'verbose_name': 'Práctica',
                'verbose_name_plural': 'Prácticas',
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reactivo', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('rfc', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('num_empleado', models.IntegerField(verbose_name='Número de Empleado')),
                ('correo_e', models.EmailField(max_length=200, verbose_name='Correo Electrónico')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Creado el')),
                ('telefono_casa', models.CharField(max_length=14)),
                ('telefono_oficina', models.CharField(max_length=14)),
                ('id_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera')),
            ],
            options={
                'verbose_name': 'Profesor',
                'verbose_name_plural': 'Profesores',
            },
        ),
        migrations.CreateModel(
            name='Respuesta_Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=20)),
                ('porque', models.CharField(max_length=500)),
                ('id_Encuesta_Alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Encuesta_Alumno')),
                ('id_pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Pregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta_Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=20)),
                ('porque', models.CharField(max_length=500)),
                ('id_Encuesta_Profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Encuesta_Profesor')),
                ('id_pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Pregunta')),
            ],
        ),
        migrations.CreateModel(
            name='SecretarioTecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=20)),
                ('num_empleado', models.IntegerField()),
                ('correo_e', models.CharField(max_length=200)),
                ('telefono_casa', models.CharField(max_length=14)),
                ('telefono_oficina', models.CharField(max_length=14)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Creado el')),
                ('id_carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera')),
            ],
            options={
                'verbose_name': 'Secretario Técnico',
                'verbose_name_plural': 'Secretarios Técnico',
            },
        ),
        migrations.CreateModel(
            name='Tipo_Limite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('E_A', 'Encuesta Alumno'), ('E_P', 'Encuesta Profesor'), ('R_P', 'Reagendar_Practica')], default='Enc_Alumno', max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('clave', models.IntegerField(primary_key=True, serialize=False)),
                ('valor', models.CharField(max_length=100, verbose_name='Turno')),
            ],
        ),
        migrations.AddField(
            model_name='pregunta',
            name='id_tipo_respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Tipo_Respuesta'),
        ),
        migrations.AddField(
            model_name='laboratorio_horario',
            name='id_clave_mat_lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Materia_Laboratorio', verbose_name='Clave Materia'),
        ),
        migrations.AddField(
            model_name='laboratorio_horario',
            name='id_grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Grupos_Carrera', verbose_name='Grupo'),
        ),
        migrations.AddField(
            model_name='laboratorio_horario',
            name='periodo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Periodo', verbose_name='Periodo'),
        ),
        migrations.AddField(
            model_name='laboratorio_horario',
            name='rfc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Profesor', verbose_name='Profesor'),
        ),
        migrations.AddField(
            model_name='jefe_materias',
            name='id_jefe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.JefeSeccion', verbose_name='Jefe de Sección'),
        ),
        migrations.AddField(
            model_name='jefe_materias',
            name='id_materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Materia_Laboratorio', verbose_name='Materia Laboratorio'),
        ),
        migrations.AddField(
            model_name='jefe_laboratorios',
            name='id_jefe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.JefeSeccion', verbose_name='Jefe de Sección'),
        ),
        migrations.AddField(
            model_name='jefe_laboratorios',
            name='id_laboratorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorio', verbose_name='Laboratorio'),
        ),
        migrations.AddField(
            model_name='horarios_clase',
            name='laboratorio_horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorio_Horario', verbose_name='Horario Laboratorio'),
        ),
        migrations.AddField(
            model_name='grupos_carrera',
            name='id_turno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Turno', verbose_name='Turno'),
        ),
        migrations.AddField(
            model_name='fecha_limite',
            name='id_tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Tipo_Limite', verbose_name='Límite para'),
        ),
        migrations.AddField(
            model_name='encuesta_profesor',
            name='id_laboratorio_horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorio_Horario'),
        ),
        migrations.AddField(
            model_name='encuesta_profesor',
            name='id_laboratorista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorista'),
        ),
        migrations.AddField(
            model_name='encuesta_profesor',
            name='id_practica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Practica'),
        ),
        migrations.AddField(
            model_name='encuesta_alumno',
            name='id_laboratorio_horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorio_Horario'),
        ),
        migrations.AddField(
            model_name='alumno_inscrito',
            name='id_laboratorio_horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorio_Horario', verbose_name='Horario Laboratorio'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='id_carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Carrera', verbose_name='Carrera'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='id_generacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Generacion', verbose_name='Generación'),
        ),
        migrations.AddField(
            model_name='agenda_practica',
            name='laboratorio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorio', verbose_name='Laboratorio'),
        ),
        migrations.AddField(
            model_name='agenda_practica',
            name='laboratorio_horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Laboratorio_Horario', verbose_name='Laboratorio Horario'),
        ),
        migrations.AddField(
            model_name='agenda_practica',
            name='practica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Practica', verbose_name='Práctica'),
        ),
        migrations.AddField(
            model_name='agenda_practica',
            name='rfc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PagGestion.Profesor', verbose_name='Profesor'),
        ),
    ]
