from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import Evento #Sherlon: Adicionado
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

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
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()

    #Valida o usuário logado, para evitar que um usuário possa deletar dados de outros usuários
    if usuario_logado == evento.usuario:
        #Realiza o DELETE no banco de dados por ID
        evento.delete()
    else:
        raise Http404()
    
    return redirect('/')

@login_required(login_url='/login/') #Demanda um usuário logado para acessar os dados do BD
def lista_eventos(request):
    data_atual = datetime.now() - timedelta(hours=1) #Define uma hora de atraso para mostrar os eventos "atrasados"
    #evento = Evento.objects.all() #Obtem TODOS os dados do BD
    evento = Evento.objects.filter(usuario=request.user)#,     #Obtem os dados do BD do USUARIO LOGADO
                                   #data_evento__gt = data_atual) #__gt significa (Maior que) e __lt significa (Menor que)
    evento = evento.order_by('data_evento') #Ordena eventos por Data
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

#Esta função se comporta como uma API. portanto não requer login de usuário.
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario) #Para autenticar remotamente pelo ID do usuário
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    dados = list(evento) #Cria uma lista a ser apresentada na web (Tipo uma API)
    return JsonResponse(dados, safe=False)