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
        verbose_name="TURNO (deja en blanco si no corresponde)",
        null=True, blank=True
        )
    
    email = models.EmailField(
        verbose_name="EMAIL  (email: ejemplo@gmail.com ---> el usuario será: ejemplo ")
    
    user = models.OneToOneField(
        User,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="worker",
        verbose_name="Empleado",
        editable=False)

    def __str__(self):
        return self.email.split("@")[0]
    
    class Meta:
        verbose_name = "Empleado"
  
           
    def save(self, *args, **kwargs):
        if not self.user: 
            self.user = User.objects.create_user(
                username = self.email.split("@")[0],
                email = self.email,
                password = "planB",
                first_name = '',
                last_name = '',
                is_active = True,
                is_staff = True,
            )
            self.id = self.user.id
            self.user.save()
        super().save(*args, **kwargs)



class Punto(models.Model):
    nombre = models.CharField(
        max_length = 100,
        null = False,
        blank = False,
        verbose_name = "Punto de Control"
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
    
    
    
        
    def save(self, *args, **kwargs):
        self.url = f"https://localhost:8000/send/{self.id}"
        self.qr = generate_qr_code_url(self.url)
        
        super().save(*args, **kwargs)

        
        
    def __str__ (self):
        return self.nombre
    
    
class Registro(models.Model):    
    worker = models.ForeignKey(
        Worker,
        related_name="registro",
        on_delete=models.CASCADE
        )
    datetime = models.DateTimeField(
        auto_now_add=True
        )
    punto = models.ForeignKey(
        Punto,
        on_delete=models.CASCADE,
        related_name="registro"
        )
    
    def __str__ (self):
        return f"{self.datetime.strftime('%d/%m/%Y %H:%M')}: {self.worker} point {self.punto}"
    