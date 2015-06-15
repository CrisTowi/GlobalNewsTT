from Principal.models import Usuario, Nota, ReporteUsuario, ReporteNota, Seccion, UsuarioSigueUsuario, Comentario, UsuarioSigueSeccion, Subseccion, Chat, MensajeDirecto
from rest_framework import serializers


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('url','username','nombre','ap_paterno','ap_materno','correo','foto','estado', )

class UsuarioSigueUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSigueUsuario

class UsuarioSigueSeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSigueSeccion

class SubseccionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subseccion

class NotaSerializer(serializers.ModelSerializer):

    usuario = serializers.ReadOnlyField(source='usuario.username')
    fecha = serializers.ReadOnlyField(source='formato_fecha')
    seccion = serializers.ReadOnlyField(source='subseccion.seccion.id')
    subseccion = serializers.ReadOnlyField(source='subseccion.id')
    likes = serializers.ReadOnlyField(source='get_likes')
    comentarios = serializers.ReadOnlyField(source='get_comentarios')
    imagen_usuario = serializers.ReadOnlyField(source='get_imagen_usuario')
    
    class Meta:
        model = Nota
        fields = ('id','usuario','seccion','subseccion','titulo','descripcion','imagen',
                            'fecha','longitud','latitud','likes','privacidad','comentarios','imagen_usuario' )

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
        fields = ('url','nombre','imagen',)

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat

class MensajeDirectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeDirecto
