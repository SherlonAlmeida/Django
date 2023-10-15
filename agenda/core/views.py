from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import Evento #Sherlon: Adicionado
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def eventos(request, titulo_evento):
    objeto = Evento.objects.get(titulo = titulo_evento)
    mensagem = f"Teste --{objeto.descricao}--"
    return HttpResponse("<h1>" + mensagem + "</h1>")

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request) #Limpa a sessão do usuário atual ao realizar logout do sistema
    return redirect('/')

def submit_login(request):
    if request.POST: 
        #Se for uma requisição POST válida, obtém os dados enviados do Form html pelo campo "name" definido
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
        else:
            messages.error(request, "Usuário ou senha inválida!")
    
    return redirect('/') #Volta para a página de login

def submit_evento(request):
    if request.POST:
        titulo = request.POST.get("titulo")
        data_evento = request.POST.get("data_evento")
        descricao = request.POST.get("descricao")
        usuario = request.user
        
        #Realiza o INSERT no banco de dados
        Evento.objects.create(titulo=titulo,
                              data_evento=data_evento,
                              descricao=descricao,
                              usuario=usuario)
    
    return redirect('/')

@login_required(login_url='/login/') #Demanda um usuário logado para acessar os dados do BD
def lista_eventos(request):
    #evento = Evento.objects.all() #Obtem TODOS os dados do BD
    evento = Evento.objects.filter(usuario=request.user) #Obtem os dados do BD do USUARIO LOGADO
    dados = {'eventos': evento}
    return render(request, "agenda.html", dados)

@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')