from django.contrib import admin

from .models import Usuario, Entrenador, Categoria, Jugador, Pago
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

# Aqui vemos lo que se puede administrar desde el panel admin
# desde el admin podemos ver los modelos que hemos creado

#MODELOS EN ADMIN
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('rol', {'fields': ('rol',)}),
    )

#Modelo de entrenador
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'usuario','ver_foto']
    fields = ['usuario', 'nombre_completo', 'telefono', 'foto']

    def ver_foto(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />')
        return "Sin foto"
    ver_foto.short_description = 'Foto'

#modelo historial de pagos
class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1

#modelo de jugador 
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'numero_playera', 'categoria', 'entrenador']
    list_filter= ['categoria', 'entrenador']
    search_fields = ['nombre_completo', 'numero_playera']
    inlines = [PagoInline]

    fields = [
        'nombre_completo', 'fecha_nacimiento', 'posicion', 'numero_playera',
        'talla_playera', 'usa_licra', 'talla_short', 'talla_licra',
        'foto', 'curp', 'acta_nacimiento',
        'telefono_tutor', 'observaciones',
        'entrenador', 'categoria'
    ]

    def edad(self, obj):
        return obj.edad()
    edad.short_description = 'Edad'

    def ver_foto(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />')
        return 'sin foto'
    ver_foto.short_description= 'Foto'


#modelo de pago
class PagoAdmin(admin.ModelAdmin):
    list_display=['jugador','mes_correspondiente', 'concepto','monto', 'estado', 'fecha_pago']
    list_filter=['concepto', 'estado','mes_correspondiente']
    search_fields=['jugador_nombre_completo','mes_correspondiente']



admin.site.register(Pago, PagoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Entrenador, EntrenadorAdmin)
admin.site.register(Categoria)
admin.site.register(Jugador, JugadorAdmin)