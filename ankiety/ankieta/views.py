from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Pytanie


def index(request):
    ostatnie_pytania_lista = Pytanie.objects.order_by('-pub_data')[:5]
    szablon = loader.get_template('ankieta/index.html')
    kontekst = {
        'ostatnie_pytania_lista': ostatnie_pytania_lista,
    }
    return HttpResponse(szablon.render(kontekst, request))

def szczegoly(request, pytanie_id):
    return HttpResponse("Przeglądasz pytanie %s." % pytanie_id)

def wyniki(request, pytanie_id):
    response = "Przeglądasz wyniki pytania %s."
    return HttpResponse(response % pytanie_id)

def glos(request, pytanie_id):
    return HttpResponse("Głosujesz na pytanie %s." % pytanie_id)
