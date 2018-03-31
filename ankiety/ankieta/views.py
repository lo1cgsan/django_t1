# from django.http import Http404
from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.template import loader
from django.views import generic
from django.utils import timezone

from .models import Pytanie, Odpowiedz


class IndexView(generic.ListView):
    """Zwraca 5 ostatnio opublikowanych ankiet (bez ankiet opublikowanych w przyszłości)"""
    template_name = 'ankieta/index.html'
    context_object_name = 'ostatnie_pytania_lista'

    def get_queryset(self):
        """Zwraca 5 ostatnio opublikowanych ankiet"""
        return Pytanie.objects.filter(
            pub_data__lte=timezone.now()
        ).order_by('-pub_data')[:5]


class SzczegolyView(generic.DetailView):
    model = Pytanie
    template_name = 'ankieta/szczegoly.html'

    def get_queryset(self):
       """
       Wykluczenie wszystkich nieopublikowanych jeszcze pytań
       """
       return Pytanie.objects.filter(pub_data__lte=timezone.now())


class WynikiView(generic.DetailView):
    model = Pytanie
    template_name = 'ankieta/wyniki.html'


def glos(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    try:
        wybrana_odpowiedz = pytanie.odpowiedz_set.get(pk=request.POST['odpowiedz'])
    except (KeyError, Odpowiedz.DoesNotExist):
        # Redisplay the pytanie voting form.
        return render(request, 'ankieta/szczegoly.html', {
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
