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
        local = request.POST.get("local")
        data_evento = request.POST.get("data_evento")
        descricao = request.POST.get("descricao")
        usuario = request.user
        
        id_evento = request.POST.get("id_evento")
        #Se o id_evento existir, apenas altera o registro no banco de dados.
        if id_evento:
            #Realiza o UPDATE no banco de dados
            #Forma 1: usando o .get() + .save()
            evento = Evento.objects.get(id=id_evento)
            if usuario == evento.usuario:
                evento.titulo = titulo
                evento.local = local
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save() #Modifica o registro no BD
            """ #Forma 2: usando o .update()
            Evento.objects.filter(id=id_evento).update(
                titulo=titulo,
                local=local,
                data_evento=data_evento,
                descricao=descricao)"""
        #Caso contrário, ele não existe, portanto insere no banco de dados.
        else:
            #Realiza o INSERT no banco de dados
            Evento.objects.create(
                titulo=titulo,
                local=local,
                data_evento=data_evento,
                descricao=descricao,
                usuario=usuario)
    
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario_logado = request.user
    
    #Obtem o evento a ser excluido
    evento = Evento.objects.get(id=id_evento)

    #Valida o usuário logado, para evitar que um usuário possa deletar dados de outros usuários
    if usuario_logado == evento.usuario:
        #Realiza o DELETE no banco de dados por ID
        evento.delete()
    
    return redirect('/')

@login_required(login_url='/login/') #Demanda um usuário logado para acessar os dados do BD
def lista_eventos(request):
    #evento = Evento.objects.all() #Obtem TODOS os dados do BD
    evento = Evento.objects.filter(usuario=request.user) #Obtem os dados do BD do USUARIO LOGADO
    dados = {'eventos': evento}
    return render(request, "agenda.html", dados)

@login_required(login_url='/login/')
def evento(request):
    #Se houver um dado cadastrado com o ID enviado via GET, podemos atualizar os dados do banco.
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)