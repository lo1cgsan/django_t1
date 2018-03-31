import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Pytanie


class PytanieModelTests(TestCase):

    def test_opublikowane_ostatnio_z_pytaniem_w_przyszlosci(self):
        """
        opublikowane_ostatnio() zwracać ma False dla pytań z pub_data
        w przyszłości.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        przyszle_pytanie = Pytanie(pub_data=time)
        self.assertIs(przyszle_pytanie.opublikowane_ostatnio(), False)

    def test_opublikowane_ostatnio_z_stare_pytanie(self):
        """
        opublikowane_ostatnio() zwracać ma False dla pytań których pub_data
        jest starsza niż 1 dzień.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        stare_pytanie = Pytanie(pub_data=time)
        self.assertIs(stare_pytanie.opublikowane_ostatnio(), False)

    def test_opublikowane_ostatnio_z_ostatnie_pytanie(self):
        """
        opublikowane_ostatnio() zwracać ma True dla pytań których pub_data
        jest w ciągu ostatniego dnia.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        ostatnie_pytanie = Pytanie(pub_data=time)
        self.assertIs(ostatnie_pytanie.opublikowane_ostatnio(), True)

def create_pytanie(pytanie_tekst, days):
    """
    Tworzy Pytanie z podanym tekstem i publikuje z datą przesuniętą
    o podaną ilość dni ujemną w przeszłość lub dodatnią w przyszłość.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Pytanie.objects.create(pytanie_tekst=pytanie_tekst, pub_data=time)


class PytanieIndexViewTests(TestCase):
    def test_brak_pytan(self):
        """
        Jeżeli brak bytań, wyświetlany jest komunikat.
        """
        response = self.client.get(reverse('ankieta:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['ostatnie_pytania_lista'], [])

    def test_przeszle_pytanie(self):
        """
        Pytania z datą w przeszłości wyświetlane są na stronie index.
        """
        create_pytanie(pytanie_tekst="Przeszłe pytanie.", days=-30)
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
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['ostatnie_pytania_lista'], [])

    def test_przyszle_pytanie_and_past_pytanie(self):
        """
        Jeżeli istnieją pytania przeszłe i przyszłe, tylko przeszłe
        są wyświetlane.
        """
        create_pytanie(pytanie_tekst="Przeszłe pytanie.", days=-30)
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
        create_pytanie(pytanie_tekst="Przeszłe pytanie 1.", days=-30)
        create_pytanie(pytanie_tekst="Przeszłe pytanie 2.", days=-5)
        response = self.client.get(reverse('ankieta:index'))
        self.assertQuerysetEqual(
            response.context['ostatnie_pytania_lista'],
            ['<Pytanie: Przeszłe pytanie 2.>', '<Pytanie: Przeszłe pytanie 1.>']
        )


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