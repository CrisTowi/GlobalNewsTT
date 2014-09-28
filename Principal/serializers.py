from Principal.models import Usuario, Nota, ReporteUsuario, ReporteNota, Seccion
from rest_framework import serializers

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('url','username','ap_paterno','ap_materno','correo','foto','estado', )

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ('usuario','subseccion','titulo','descripcion','imagen',
        					'facha','longitud','latitud','imagen','likes', 'privacidad', )

class ComentarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Nota
        fields = ('url','usuario','nota','contenido','fecha',)

class ReporteUsuarioSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ReporteUsuario
		fields = ('url','usuario_reportado','usuario_reportador','tipo','fecha',)

class ReporteNotaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ReporteNota
		fields = ('url','usuario','nota','tipo','fecha',)

class SeccionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Seccion
		fields = ('url','nombre',)
