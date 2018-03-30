# from django.http import Http404
from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.template import loader

from .models import Pytanie, Odpowiedz


def index(request):
    ostatnie_pytania_lista = Pytanie.objects.order_by('-pub_data')[:5]
    kontekst = {'ostatnie_pytania_lista': ostatnie_pytania_lista}
    return render(request, 'ankieta/index.html', kontekst)

def szczegoly(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    return render(request, 'ankieta/szczegoly.html', {'pytanie':pytanie})

def wyniki(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    return render(request, 'ankieta/wyniki.html', {'pytanie':pytanie})

def glos(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    try:
        wybrana_odpowiedz = pytanie.odpowiedz_set.get(pk=request.POST['odpowiedz'])
    except (KeyError, Odpowiedz.DoesNotExist):
        # Redisplay the pytanie voting form.
        return render(request, 'polls/szczegoly.html', {
            'pytanie': pytanie,
            'blad_tekst': "Nie wybrałeś odpowiedzi.",
        })
    else:
        wybrana_odpowiedz.glosy += 1
        wybrana_odpowiedz.save()
        # Zawsze zwracaj HttpResponseRedirect po poprawnym obsłużeniu żądania POST
        # z danymi. Zapobiega to dwukrotnemu przesyłaniu danych, gdyby użytkownik
        # nacisnął przycisk wstecz.
        return HttpResponseRedirect(reverse('ankieta:wyniki', args=(pytanie.id,)))
