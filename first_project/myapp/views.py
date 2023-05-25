from django.shortcuts import render

# Create your views here.

#Sherlon: Adicionei o código do "Olá Mundo" abaixo
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Olá, Mundo!")