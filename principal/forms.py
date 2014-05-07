from django.forms import ModelForm
from django import forms
from principal.models import Entrada, Comentario

class ContactoForm(forms.Form):
	correo = forms.EmailField(label='Tu correo electronico')
	mensaje = forms.CharField(widget=forms.Textarea)

class EntradaForm(ModelForm):
	class Meta:
		model=Entrada
		exclude=['usuario','votos']


class ComentarioForm(ModelForm):
	class Meta:
		model= Comentario
		exclude=['entrada','usuario']
