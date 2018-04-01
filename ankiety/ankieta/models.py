import datetime

from django.db import models
from django.utils import timezone

class Pytanie(models.Model):
    pytanie_tekst = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data publikacji')

    def __str__(self):
        """reprezentacja obiektu"""
        return self.pytanie_tekst

    @property
    def opublikowane_ostatnio(self):
        teraz = timezone.now()
        return teraz - datetime.timedelta(days=1) <= self.pub_data <= teraz

    def ma_odpowiedzi(self):
        return self.odpowiedz_set.all().count()

class Odpowiedz(models.Model):
    pytanie = models.ForeignKey(Pytanie, on_delete=models.CASCADE)
    wybor_tekst = models.CharField(max_length=200)
    glosy = models.IntegerField(default=0)

    def __str__(self):
        return self.wybor_tekst