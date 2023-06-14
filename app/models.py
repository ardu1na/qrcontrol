from django.db import models

from django.contrib.auth.models import User





class Worker(models.Model):
    SHIFT_CHOICES = (
        ('DIA', 'Día'),
        ('NOCHE', 'Noche'),
    )

    shift = models.CharField(
        max_length=20, choices=SHIFT_CHOICES, verbose_name="Turno")
    
    email = models.EmailField(
        verbose_name="Correo electrónico")
    
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name="worker", verbose_name="Empleado")

    def __str__(self):
        return self.email.split("@")[0]
  
           
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
        blank = False
        )
    url = models.URLField(
        blank = True,
        null = True
        )
    
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
    