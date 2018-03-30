import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Pytanie


class PytanieModelTests(TestCase):

    def test_opublikowany_ostatnio_z_pytaniem_w_przyszlosci(self):
        """
        opublikowane_ostatnio() zwraca False dla pytań z pub_data
        w przyszłości.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        przyszle_pytanie = Pytanie(pub_data=time)
        self.assertIs(przyszle_pytanie.opublikowane_ostatnio(), False)