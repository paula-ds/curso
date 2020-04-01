from django.conf.urls import url
from capitulos.views import hello_world, home2,home3, home4,buscador #importar funciones

urlpatterns = [
            url(regex=r'^(?P<capitulo>\w+)/$', view=home2, name='home2'),
            url(regex=r'caracter/(?P<personaje>\w+)/$', view=home3, name='home3'),
            url(regex=r'location/(?P<locacion>\w+)/$', view=home4, name='home4'),
            url(regex= r'^$',view=hello_world, name= 'hola')
  
]
