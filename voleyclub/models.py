from django.db import models
from datetime import  date
#esta importacion es para el usuario personalizado
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

#molde de usuario personalizado
class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('admin', 'Administrador'),
        ('entrenador', 'Entrenador'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='entrenador')
    
    def __str__(self):
        return f"{self.username} ({self.rol})"

#molde de entrenador
class Entrenador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    foto = models.ImageField(upload_to='entrenadores/', blank=True, null=True)

    def __str__(self):
        return self.nombre_completo
    
#molde de categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    año_inicio = models.IntegerField()
    año_fin = models.IntegerField()

    def __str__(self):
        return self.nombre

#molde de jugador
class Jugador(models.Model):
    TALLAS_CHOICES = [
        ('2', '2'),
        ('4', '4'),
        ('6', '6'),
        ('8', '8'),
        ('10', '10'),
        ('12', '12'),
        ('14', '14'),
        ('16', '16'),
        ('ch', 'Chico'),
        ('m', 'Mediano'),
        ('g', 'Grande'),
        ('Xg', 'Extra Grande'),
        ('XXg', 'Doble Extra Grande'),
    ]

    nombre_completo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    posicion = models.CharField(max_length=50)
    fecha_inscripcion = models.DateField(auto_now=True)
    observaciones = models.TextField(blank=True, null=True)
    telefono_tutor = models.CharField(max_length=15, blank=True, null=True)
    numero_playera = models.PositiveIntegerField(unique=False, null=True, blank=True)
    foto = models.ImageField(upload_to='jugadores/', blank=True, null=True)
    curp = models.FileField(upload_to='jugadores/curp/', blank=True, null=True)
    acta_nacimiento = models.FileField(upload_to='jugadores/acta_nacimiento/', blank=True, null=True)
    

    # tallas de uniforme con opciones predefinidas
    talla_playera = models.CharField(max_length=10, choices=TALLAS_CHOICES)
    usa_licra = models.BooleanField(default=False, help_text="Marca si usa licra en lugar de short.")
    talla_short = models.CharField(max_length=10, choices=TALLAS_CHOICES, blank=True, null=True)
    talla_licra = models.CharField(max_length=10, choices=TALLAS_CHOICES, blank=True, null=True)


    # relacion con el entrenador y la categoria 
    entrenador = models.ForeignKey('Entrenador', on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)

    # calcular la edad del jugador
    def calcular_edad(self):
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def clean(self):
        super().clean()

        if self.usa_licra:
          if not self.talla_licra:
            raise ValidationError("Selecciona una talla de licra si el jugador usa licra.")
          if self.talla_short:
            raise ValidationError("No llenes talla de short si el jugador usa licra.")
        else:
          if not self.talla_short:
            raise ValidationError("Selecciona una talla de short si el jugador no usa licra.")
          if self.talla_licra:
            raise ValidationError("No llenes talla de licra si el jugador no usa licra.")
          
    # metodo para obtener la categoria del jugador
    def save(self, *args, **kwargs):
        edad = self.calcular_edad()

        if edad <= 11:
            nombre_categoria = 'Mini Voleibol'
        elif edad in [12, 13]:
            nombre_categoria = 'Infantil Menor'
        elif edad in [14, 15]:
            nombre_categoria =	'Infantil Mayor'
        elif edad in [16, 17]:
            nombre_categoria ='Juvenil Menor' 
        elif edad in [18, 19]:
            nombre_categoria = 'Juvenil Mayor'
        elif edad in [20, 21]:
            nombre_categoria = 'Juvenil Superior'
        else:
            nombre_categoria = 'Libre'

        try:
            categoria_obj= Categoria.objects.get(nombre=nombre_categoria)
            self.categoria = categoria_obj 
        except Categoria.DoesNotExist:
            self.categoria = None

        super().save(*args, **kwargs)        

    def __str__(self):
        return self.nombre_completo
    
#molde de pago

class Pago(models.Model):
    CONCEPTO_CHOICES = (
        ('inscripcion', 'Inscripción'),
        ('mensualidad', 'Mensualidad'),
        ('uniforme', 'Uniforme'),
        ('evento', 'Evento'),
        ('otro', 'Otro'),
    )

    ESTADO_CHOICES= (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    )

    MES_CHOICES = (
        ('enero', 'Enero'),
        ('febrero', 'Febrero'),
        ('marzo', 'Marzo'),
        ('abril', 'Abril'),
        ('mayo', 'Mayo'),
        ('junio', 'Junio'),
        ('julio', 'Julio'),
        ('agosto', 'Agosto'),
        ('septiembre', 'Septiembre'),
        ('octubre', 'Octubre'),
        ('noviembre', 'Noviembre'),
        ('diciembre', 'Diciembre'),
    )

    jugador= models.ForeignKey('Jugador', on_delete=models.CASCADE,related_name= 'pagos')
    fecha_pago =models.DateField(auto_now=True)
    mes_correspondiente= models.CharField(max_length=20, choices=MES_CHOICES)
    concepto= models.CharField(max_length=20 , choices=CONCEPTO_CHOICES)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES,default='pendiente')

    def __str__(self):
        return f"{self.jugador.nombre_completo} - {self.mes_correspondiente} - {self.concepto}"

