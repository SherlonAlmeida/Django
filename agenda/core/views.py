from django.shortcuts import render
from django.http import HttpResponse
from core.models import Evento #Sherlon: Adicionado

# Create your views here.

def eventos(request, titulo_evento):
    objeto = Evento.objects.get(titulo = titulo_evento)
    mensagem = f"Teste --{objeto.descricao}--"
    return HttpResponse("<h1>" + mensagem + "</h1>")

def lista_eventos(request):
    evento = Evento.objects.all() #Obtem TODOS os dados do BD
    #evento = Evento.objects.filter(usuario=request.user) #Obtem os dados do BD do USUARIO LOGADO
    dados = {'eventos': evento}
    return render(request, "agenda.html", dados)