from Principal.models import Usuario, Nota, ReporteUsuario, ReporteNota, Seccion, UsuarioSigueUsuario, Comentario
from rest_framework import serializers


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('url','username','nombre','ap_paterno','ap_materno','correo','foto','estado', )

class UsuarioSigueUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSigueUsuario

class NotaSerializer(serializers.ModelSerializer):

    usuario = serializers.Field(source='usuario.username')
    fecha = serializers.Field(source='formato_fecha')
    seccion = serializers.Field(source='subseccion.seccion.id')
    likes = serializers.Field(source='num_likes')
    comentarios = serializers.Field(source='get_comentarios')
    
    class Meta:
        model = Nota
        fields = ('id','usuario','seccion','subseccion','titulo','descripcion','imagen',
        					'fecha','longitud','latitud','likes','privacidad','comentarios', )

class ComentarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comentario
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
