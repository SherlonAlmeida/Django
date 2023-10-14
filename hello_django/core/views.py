from django.shortcuts import render, HttpResponse

# Create your views here.

def hello(requests):
    return HttpResponse("<h1>Hello World!</h1>")