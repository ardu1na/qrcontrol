
from django.urls import path
from app import views

urlpatterns = [
    path('control/', views.qrs, name="qrs"), # print qr code 
    path('send/<int:id>/', views.send, name="send"), # send point request
    path('', views.index, name="index") 

]
