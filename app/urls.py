
from django.urls import path
from app import views

urlpatterns = [
    path('send/<int:id>/', views.send_request, name="send") # send point request
    
]
