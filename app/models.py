from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


def generate_qr_code_url(url, size=300):
    
    base_url = 'https://chart.googleapis.com/chart'
    params = {
        'cht': 'qr',
        'chs': f'{size}x{size}',
        'chl': url
    }
    qr_code_url = f'{base_url}?{"&".join(f"{key}={value}" for key, value in params.items())}'
    return qr_code_url



class Worker(models.Model):
    SHIFT_CHOICES = (
        ('DIA', 'Día'),
        ('NOCHE', 'Noche'),
    )

    shift = models.CharField(
        max_length=20,
        choices=SHIFT_CHOICES,
        verbose_name="TURNO",
        null=True, blank=True,
        help_text= "(deja en blanco si no corresponde)",

        )
    
    KIND_CHOICES = (
        ('EMPLEADO', 'Empleado'),
        ('SERENO', 'Sereno'),
    )
    
    kind = models.CharField(
        max_length=20,
        choices=KIND_CHOICES,
        verbose_name="CATEGORÍA",
        help_text= "(deja en blanco si no corresponde)",
        null=True, blank=True
        )
    
    email = models.EmailField(
        verbose_name="EMAIL")
    
    telefono = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="N° TELÉFONO"
    )
    nombre = models.CharField(
        max_length=90,
        null=True, blank=True,
        verbose_name="NOMBRE"
        )
    
    apellido = models.CharField(
        max_length=90,
        verbose_name="APELLIDO",
        null=True, blank=True
        )
    
    user = models.OneToOneField(
        User,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="worker",
        verbose_name="USERNAME",
        editable=False)

    def __str__(self):
        if self.nombre and self.apellido:
            return f'{self.nombre} {self.apellido}'
        else:
            return self.email.split("@")[0]
    
    class Meta:
        verbose_name = "Empleado"
  
           
    def save(self, *args, **kwargs):
        
        if not self.user: 
            self.user = User.objects.create_user(
                username = self.email,
                email = self.email,
                password = "planB",
                first_name = '',
                last_name = '',
                is_active = True,
                is_staff = True,
            )
            self.user.save()
        super().save(*args, **kwargs)



class Punto(models.Model):
    nombre = models.CharField(
        max_length = 100,
        null = False,
        blank = False,
        verbose_name = "Punto de Control",
        unique=True,
        )
    url = models.URLField(
        blank = True,
        null = True,

        )
    qr = models.URLField(
        blank = True,
        null = True,
        verbose_name="QR"
        )
    
    
    
        
    def save(self, *args, **kwargs): # aqui hay que hacer que guarde y despues añada el id
        if not self.pk:    
            super().save(*args, **kwargs) 
        self.url = f'https://localhost:8000/send/{self.id}/'
        self.qr = generate_qr_code_url(self.url)
        
        super().save(*args, **kwargs)

        
        
    def __str__ (self):
        return self.nombre
    
    
class Registro(models.Model):    
    worker = models.ForeignKey(
        Worker,
        related_name="registro",
        on_delete=models.CASCADE,
        verbose_name="EMPLEADO"
        )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name="FECHA Y HORA"
        )
    punto = models.ForeignKey(
        Punto,
        on_delete=models.CASCADE,
        related_name="registro",
        verbose_name= "PUNTO DE CONTROL"
        )
    
    def __str__ (self):
        return f"{self.datetime.strftime('%d/%m/%Y %H:%M')}: {self.worker} point {self.punto}"
    