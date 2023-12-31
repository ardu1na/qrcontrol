from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required



from app.models import Worker, Punto, Registro


def error404(request, exception):
        data = {}
        return render(request,'404.html', data)



def error500(request):
    data = {}
    return render(request,'500.html', data)

@login_required 
def index(request):
    return render(request, 'index.html', {})


@login_required 
def qrs(request):
    puntos = Punto.objects.all()
    context={
        'puntos':puntos,
    }
    return render(request, 'qr.html', context)



# ####################
# LOGICA PARA EL REGISTRO DE LOS SERENOS
# PASO X PUNTOS DE CONTROL
#

# requiere estar loggeado
# sino lleva a la pag del login
@login_required 
def send(request, id):
    # solicita el id del punto de control
    # EL ID va como parámetro en el qr
    
    # identifica el trabajador en base al usuario loggeado
    worker_id = request.user.id
    worker = get_object_or_404(Worker, id=worker_id)
    print(worker)
    
    # identifica al punto de control 
    punto = get_object_or_404(Punto, id=id)
    print(punto)
    
    # crea el registro
    # para el empleado, en ese momento, en ese punto de control
    new_registro = Registro.objects.create(worker=worker, punto=punto)
    print(new_registro)
    
    return redirect('success')



@login_required 
def success(request):
    html_template = 'success.html'
    # respuesta al usuario
    return render(request, html_template, {})
#
# ####################


