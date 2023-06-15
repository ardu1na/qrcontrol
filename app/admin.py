from django.contrib import admin
from django.utils.html import format_html
from django import forms
from import_export.admin import ImportExportModelAdmin

from app.models import Worker, Punto, Registro
from app.resources import RegistroResource


class ImageURLWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value:
            return html + format_html('<br><img src="{}" width="200" height="200" />', value)
        else:
            return html
        

class PuntoAdminForm(forms.ModelForm):
    qr = forms.URLField(widget=ImageURLWidget, required=False, help_text="QR LINK PARA IMPRIMIR - DEJA EN BLANCO - SE COMPLETARÁ AUTOMATICAMENTE", label="QR")

    class Meta:
        model = Punto
        fields = ['nombre', 'qr']        
        

class PuntoAdmin(admin.ModelAdmin):
    form = PuntoAdminForm
    list_display = ('nombre', 'display_qr_image')
    readonly_fields = ('qr',)
    
    def display_qr_image(self, obj):
        if obj.qr:
            return format_html('<img src="{}" width="250" height="250" />', obj.qr)
        else:
            return ''

    display_qr_image.short_description = 'QR Code '
    
    
    fieldsets = (
        (None, {'fields': ('nombre', 'qr')},
         ),
        ('IMPRIMIR QR', {'fields': () , 'description': 'Para imprimir los código QR puedes ir a https://granjapicodorado.pythoanywhere.com/control'}
         ),
    )
    
    
admin.site.register(Punto, PuntoAdmin)




class RegistroAdmin(ImportExportModelAdmin):
    list_display = ('datetime', 'punto', 'worker' )
    list_filter = ('worker', 'punto')
    list_per_page =  10
    date_hierarchy = 'datetime'
    resource_class = RegistroResource

admin.site.register(Registro, RegistroAdmin)


# Lib\site-packages\jazzmin\templates\admin\base.html borrrar el footer

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'nombre', 'apellido')
    fieldsets = (
        (None, {'fields': ('shift', 'apellido', 'nombre', 'email')},
         ),
        ('CONTRASEÑA', {'fields': () , 'description': 'Atención! "planB" es la contraseña. PERO pidele a tu empleado que la cambie para mayor seguridad. El USERNAME será la primera parte del email.'}
         ),
    )

admin.site.register(Worker, WorkerAdmin)





