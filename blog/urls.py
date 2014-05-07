from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.foo.urls')),
    url(r'^$', 'principal.views.lista_entradas'),
    url(r'^sobre/$', 'principal.views.sobre'),
    url(r'^usuarios/$', 'principal.views.usuarios'),
    url(r'^contacto/$', 'principal.views.contacto'),
    url(r'^privado/$','principal.views.privado'),
    url(r'^cerrar/$','principal.views.cerrar'),
    url(r'^entrada/nueva/$', 'principal.views.nueva_entrada'),
    url(r'^usuario/nuevo$', 'principal.views.nuevo_usuario'),
    url(r'^comenta/$', 'principal.views.nuevo_comentario'),
    url(r'^ingresar/$', 'principal.views.ingresar'),
    url(r'^perfil/$', 'principal.views.perfil'),
    #url(r'^entradas/', 'principal.views.lista_entradas'),
    url(r'^entrada/(?P<id_entrada>\d+)$','principal.views.detalle_entrada'),
    url(r'^borrar/entrada/(?P<id_entrada>\d+)$','principal.views.borrar_entrada'),
    url(r'^voto/positivo/(?P<id_entrada>\d+)$','principal.views.voto_positivo'),
    url(r'^voto/negativo/(?P<id_entrada>\d+)$','principal.views.voto_negativo'),
    url(r'^administrar/usuarios$','principal.views.adminusuarios'),
    url(r'^administrar/usuariosstaff(?P<id_usuario>\d+)$','principal.views.staff'),
    url(r'^administrar/usuariosnostaff(?P<id_usuario>\d+)$','principal.views.nostaff'),
    url(r'^modificar/entrada/(?P<id_entrada>\d+)$','principal.views.modificar_entrada'),
    url(r'^modificar/comentario/(?P<id_comentario>\d+)$','principal.views.modificar_comentario'),
    url(r'^borrar/comentario/(?P<id_comentario>\d+)$','principal.views.borrar_comentario'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
