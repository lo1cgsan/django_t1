from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Witaj świecie!")

def szczegoly(request, pytanie_id):
    return HttpResponse("Przeglądasz pytanie %s." % pytanie_id)

def wyniki(request, pytanie_id):
    response = "Przeglądasz wyniki pytania %s."
    return HttpResponse(response % pytanie_id)

def glos(request, pytanie_id):
    return HttpResponse("Głosujesz na pytanie %s." % pytanie_id)
