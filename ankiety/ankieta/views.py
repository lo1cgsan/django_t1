from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader

from .models import Pytanie


def index(request):
    ostatnie_pytania_lista = Pytanie.objects.order_by('-pub_data')[:5]
    kontekst = {'ostatnie_pytania_lista': ostatnie_pytania_lista}
    return render(request, 'ankieta/index.html', kontekst)

def szczegoly(request, pytanie_id):
    try:
        pytanie = Pytanie.objects.get(pk=pytanie_id)
    except Pytanie.DoesNotExist:
        raise Http404("Pytanie nie istnieje")
    return render(request, 'ankieta/szczegoly.html', {'pytanie':pytanie})

def wyniki(request, pytanie_id):
    response = "Przeglądasz wyniki pytania %s."
    return HttpResponse(response % pytanie_id)

def glos(request, pytanie_id):
    return HttpResponse("Głosujesz na pytanie %s." % pytanie_id)
