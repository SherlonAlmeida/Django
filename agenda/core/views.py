from django.shortcuts import render
from django.http import HttpResponse
from core.models import Evento #Sherlon: Adicionado

# Create your views here.

def eventos(request, titulo_evento):
    objeto = Evento.objects.get(titulo = titulo_evento)
    mensagem = f"Teste --{objeto.descricao}--"

    return HttpResponse("<h1>" + mensagem + "</h1>")