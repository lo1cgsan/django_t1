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
