from django.contrib import admin
from django.utils.html import format_html
from django import forms

from app.models import Worker, Punto, Registro




class ImageURLWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value:
            return html + format_html('<br><img src="{}" width="200" height="200" />', value)
        else:
            return html
        

class PuntoAdminForm(forms.ModelForm):
    qr = forms.URLField(widget=ImageURLWidget, required=False, help_text="QR DE CADA PUNTO DE CONTROL")

    class Meta:
        model = Punto
        fields = ['nombre', 'qr']        
        

class PuntoAdmin(admin.ModelAdmin):
    form = PuntoAdminForm
    list_display = ('nombre', 'display_qr_image')
    
    def display_qr_image(self, obj):
        if obj.qr:
            return format_html('<img src="{}" width="250" height="250" />', obj.qr)
        else:
            return ''

    display_qr_image.short_description = 'QR Code'
admin.site.register(Punto, PuntoAdmin)

admin.site.register(Registro)




class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fieldsets = (
        (None, {'fields': ('shift', 'email')},
         ),
        ('CONTRASEÑA', {'fields': () , 'description': 'Atención! "planB" es la contraseña. PERO pidele a tu empleado que la cambie para mayor seguridad. '}
         ),
    )

admin.site.register(Worker, WorkerAdmin)





