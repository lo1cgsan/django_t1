import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Pytanie, Odpowiedz


def create_pytanie(pytanie_tekst, days):
    """
    Tworzy Pytanie z podanym tekstem i publikuje z datą przesuniętą
    o podaną ilość dni ujemną w przeszłość lub dodatnią w przyszłość.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Pytanie.objects.create(pytanie_tekst=pytanie_tekst, pub_data=time)


def create_odpowiedz(pytanie, tekst):
    """
    Tworzy odpowiedz dla pytania o treści tekst
    """
    return Odpowiedz.objects.create(pytanie=pytanie, wybor_tekst=tekst)


class PytanieModelTests(TestCase):
    def test_opublikowane_ostatnio_z_pytaniem_w_przyszlosci(self):
        """
        opublikowane_ostatnio() zwracać ma False dla pytań z pub_data
        w przyszłości.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        przyszle_pytanie = Pytanie(pub_data=time)
        self.assertIs(przyszle_pytanie.opublikowane_ostatnio, False)

    def test_opublikowane_ostatnio_z_stare_pytanie(self):
        """
        opublikowane_ostatnio() zwracać ma False dla pytań których pub_data
        jest starsza niż 1 dzień.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        stare_pytanie = Pytanie(pub_data=time)
        self.assertIs(stare_pytanie.opublikowane_ostatnio, False)

    def test_opublikowane_ostatnio_z_ostatnie_pytanie(self):
        """
        opublikowane_ostatnio() zwracać ma True dla pytań których pub_data
        jest w ciągu ostatniego dnia.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        ostatnie_pytanie = Pytanie(pub_data=time)
        self.assertIs(ostatnie_pytanie.opublikowane_ostatnio, True)


class PytanieIndexViewTests(TestCase):
    def test_brak_pytan(self):
        """
        Jeżeli brak bytań, wyświetlany jest komunikat.
        """
        response = self.client.get(reverse('ankieta:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak ankiet.")
        self.assertQuerysetEqual(response.context['ostatnie_pytania_lista'], [])

    def test_przeszle_pytanie(self):
        """
        Pytania z datą w przeszłości wyświetlane są na stronie index.
        """
        p = create_pytanie(pytanie_tekst="Przeszłe pytanie.", days=-30)
        create_odpowiedz(p, "Odpowiedź")
        response = self.client.get(reverse('ankieta:index'))
        self.assertQuerysetEqual(
            response.context['ostatnie_pytania_lista'],
            ['<Pytanie: Przeszłe pytanie.>']
        )

    def test_przyszle_pytanie(self):
        """
        Pytania z datą w przyszłości nie są wyswietlane na stronie index.
        """
        create_pytanie(pytanie_tekst="Przyszłe pytanie.", days=30)
        response = self.client.get(reverse('ankieta:index'))
        self.assertContains(response, "Brak ankiet.")
        self.assertQuerysetEqual(response.context['ostatnie_pytania_lista'], [])

    def test_przyszle_pytanie_i_przeszle_pytanie(self):
        """
        Jeżeli istnieją pytania przeszłe i przyszłe, tylko przeszłe
        są wyświetlane.
        """
        p = create_pytanie(pytanie_tekst="Przeszłe pytanie.", days=-30)
        create_odpowiedz(p, "Odpowiedź")
        create_pytanie(pytanie_tekst="Przyszłe pytanie.", days=30)
        response = self.client.get(reverse('ankieta:index'))
        self.assertQuerysetEqual(
            response.context['ostatnie_pytania_lista'],
            ['<Pytanie: Przeszłe pytanie.>']
        )

    def test_dwa_przeszle_pytania(self):
        """
        Strona index może wyświetlać wiele pytań.
        """
        p1 = create_pytanie(pytanie_tekst="Przeszłe pytanie 1.", days=-30)
        create_odpowiedz(p1, "Odpowiedź")
        p2 = create_pytanie(pytanie_tekst="Przeszłe pytanie 2.", days=-5)
        create_odpowiedz(p2, "Odpowiedź")
        response = self.client.get(reverse('ankieta:index'))
        self.assertQuerysetEqual(
            response.context['ostatnie_pytania_lista'],
            ['<Pytanie: Przeszłe pytanie 2.>', '<Pytanie: Przeszłe pytanie 1.>']
        )

    def test_brak_odpowiedzi(self):
        """
        zwraca False jeśli pytanie nie ma odpowiedzi
        """
        create_pytanie(pytanie_tekst="Pytanie bez odpowiedzi.", days=0)
        response = self.client.get(reverse('ankieta:index'))
        self.assertEqual(response.context['ostatnie_pytania_lista'].count(), False)


class PytanieSzczegolyViewTests(TestCase):
    def test_przyszle_pytanie(self):
        """
        Widok szczegółowy pytania z datą przyszłą powinien zwrócić 404.
        """
        przyszle_pytanie = create_pytanie(pytanie_tekst='Przyszłe pytanie.', days=5)
        url = reverse('ankieta:szczegoly', args=(przyszle_pytanie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_przeszle_pytanie(self):
        """
        Widok szczegółowy pytania z datą przeszłą zwraca tekst pytania.
        """
        przeszle_pytanie = create_pytanie(pytanie_tekst='Przeszle Pytanie.', days=-5)
        url = reverse('ankieta:szczegoly', args=(przeszle_pytanie.id,))
        response = self.client.get(url)
        self.assertContains(response, przeszle_pytanie.pytanie_tekst)


class PytanieWynikiViewTests(TestCase):
    def test_przyszle_pytanie(self):
        """
        Widok wyników pytania z datą przyszłą powinien zwrócić 404.
        """
        przyszle_pytanie = create_pytanie(pytanie_tekst='Przyszłe pytanie.', days=5)
        url = reverse('ankieta:wyniki', args=(przyszle_pytanie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_przeszle_pytanie(self):
        """
        Widok wyników pytania z datą przeszłą zwraca tekst pytania.
        """
        przeszle_pytanie = create_pytanie(pytanie_tekst='Przeszle Pytanie.', days=-5)
        url = reverse('ankieta:wyniki', args=(przeszle_pytanie.id,))
        response = self.client.get(url)
        self.assertContains(response, przeszle_pytanie.pytanie_tekst)
