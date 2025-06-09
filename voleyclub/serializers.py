
from rest_framework import serializers
from .models import Usuario, Entrenador, Categoria, Jugador, Pago

#class UsuarioSerializer (serializers.ModelSerializer):
#    class Meta:
#        model = Usuario
#        fields = ['id', 'username', 'rol']
#
class EntrenadorSerializer (serializers.ModelSerializer):
    class Meta:
        model = Entrenador
        fields = '__all__'

class CategoriaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class JugadorSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(read_only=True)
    curp = serializers.FileField(read_only=True)
    acta_nacimiento = serializers.FileField(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    entrenador =EntrenadorSerializer(read_only=True)
    class Meta:
        model = Jugador
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

