from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from app.models import Worker, Punto, Registro


@login_required
def test(request):
    worker_id = request.user.id
    worker = get_object_or_404(Worker, id=worker_id)
    print(worker)


    return HttpResponse(f"Solicitud de {worker}")