from import_export import resources
from import_export.widgets import ForeignKeyWidget, DateTimeWidget
from import_export.fields import Field

from app.models import Registro, Worker, Punto
   



class RegistroResource(resources.ModelResource):   
    
    worker = Field(
        column_name='Empleado',
        attribute='worker',
        widget=ForeignKeyWidget(model=Worker, field='nombre'))
    
    
    punto = Field(
        column_name='Punto QR',
        attribute='punto',
        widget=ForeignKeyWidget(model=Punto, field='nombre'))
    
    
    
    datetime = Field(
        column_name='Fecha/Hora',
        attribute='datetime',
        widget=DateTimeWidget(format='%H:%M %d/%m/%Y ')) 
    
    
    
    class Meta:
        model = Registro
        fields = ('worker', 'punto', 'datetime')

        
        
            