from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from app.models import Worker, Punto, Registro


@login_required
def test(request, id):
    worker_id = request.user.id
    worker = get_object_or_404(Worker, id=worker_id)
    print(worker)
    punto = get_object_or_404(Punto, id=id)
    print(punto)
    new_registro = Registro.objects.create(worker=worker, punto=punto)
    print(new_registro)


    return HttpResponse(f"Solicitud de {worker} en {punto} \n {new_registro}")