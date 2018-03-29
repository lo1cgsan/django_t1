from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
# from django.template import loader

from .models import Pytanie


def index(request):
    ostatnie_pytania_lista = Pytanie.objects.order_by('-pub_data')[:5]
    kontekst = {'ostatnie_pytania_lista': ostatnie_pytania_lista}
    return render(request, 'ankieta/index.html', kontekst)

def szczegoly(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    return render(request, 'ankieta/szczegoly.html', {'pytanie':pytanie})

def wyniki(request, pytanie_id):
    response = "Przeglądasz wyniki pytania %s."
    return HttpResponse(response % pytanie_id)

def glos(request, pytanie_id):
    return HttpResponse("Głosujesz na pytanie %s." % pytanie_id)
