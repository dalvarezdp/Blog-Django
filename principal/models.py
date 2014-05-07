#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Entrada(models.Model):
	titulo = models.CharField(max_length=100, unique=True)
	cuerpo = models.TextField(help_text='Escribe el articulo')
	imagen = models.ImageField(upload_to='entradas',verbose_name='Imágen')
	tiempo_registro = models.DateTimeField(auto_now=True)
	usuario = models.ForeignKey(User)
	votos = models.IntegerField()
	def __unicode__(self):
		return self.titulo

class Comentario(models.Model):
	entrada = models.ForeignKey(Entrada)
	texto = models.TextField(help_text='Tu comentario', verbose_name='Comentario')
	usuario = models.ForeignKey(User)
	def __unicode__(self):
		return self.texto
