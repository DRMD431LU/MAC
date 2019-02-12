from django import forms
from .models import EncuestaProfesor, RespuestaProfesor
from django.utils.translation import ugettext_lazy as _


class PracticaForm(forms.ModelForm):

    class Meta:
        model = EncuestaProfesor
        fields = '__all__'

        widgets = {
            # 'folio': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Folio'}),
            'id_laboratorio': forms.Select(attrs={'class': 'form-control'}),
            'id_profesor': forms.Select(attrs={'class': 'form-control'}),
            'id_practica': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control'}),
        }


class PreguntasForm(forms.ModelForm):
    class Meta:
        model = RespuestaProfesor
        fields = '__all__'
        widgets = {
            'encuesta':forms.Select(attrs={'class':'form-control','id':'folio2_id'}),
            'servicio' : forms.Select(attrs={
                'class': 'form-control', }),
            'cumplio_objetivo' : forms.Select(attrs={
                'class': 'form-control',}),
            'id_laboratorista' : forms.Select(attrs={
                'class': 'form-control',}),
            'apertura_oportuna' : forms.Select(attrs={
                'class': 'form-control',}),
            'apertura_porque' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '¿Por qué?'}),
            'permanencia_enpractica' :forms.Select(attrs={
                'class': 'form-control',}),
            'permanencia_porque' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '¿Por qué?'}),
            'colaboracion_practica' :forms.Select(attrs={
                'class': 'form-control',}),
            'colaboracion_porque' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '¿Por qué?'}),
            'entrega_equipo' :forms.Select(attrs={
                'class': 'form-control',}),
            'entrega_porque' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '¿Por qué?'}),
        }
