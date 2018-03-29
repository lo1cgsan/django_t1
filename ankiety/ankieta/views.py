from django.shortcuts import render
from django.http import HttpResponse

from .models import Pytanie


def index(request):
    ostatnie_pytania_lista = Pytanie.objects.order_by('-pub_data')[:5]
    wyjscie = ', '.join([p.pytanie_tekst for p in ostatnie_pytania_lista])
    return HttpResponse(wyjscie)

def szczegoly(request, pytanie_id):
    return HttpResponse("Przeglądasz pytanie %s." % pytanie_id)

def wyniki(request, pytanie_id):
    response = "Przeglądasz wyniki pytania %s."
    return HttpResponse(response % pytanie_id)

def glos(request, pytanie_id):
    return HttpResponse("Głosujesz na pytanie %s." % pytanie_id)
