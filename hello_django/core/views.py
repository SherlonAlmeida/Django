from django.shortcuts import render, HttpResponse

# Create your views here.

#View criada para mostrar "Olá Mundo"
def hello(requests):
    return HttpResponse("<h1>Hello World!</h1>")

#View criada para uma Calculadora
def calculadora(requests, num1, num2, operacao):
    if operacao == '+':
        resultado = num1 + num2
    elif operacao == '-':
        resultado = num1 - num2
    elif operacao == '*':
        resultado = num1 * num2
    elif operacao == '%':
        resultado = num1 / num2
    else:
        return HttpResponse("Operação inválida!")    
    
    mensagem = f"A operaçãode {operacao} entre {num1} e {num2} é: {resultado}"
    return HttpResponse("<h1>"+mensagem+"</h1>")