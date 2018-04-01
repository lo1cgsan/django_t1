import datetime

from django.db import models
from django.utils import timezone

class Pytanie(models.Model):
    pytanie_tekst = models.CharField("treść pytania", max_length=200)
    pub_data = models.DateTimeField('data publikacji')

    def __str__(self):
        """reprezentacja obiektu"""
        return self.pytanie_tekst

    def opublikowane_ostatnio(self):
        teraz = timezone.now()
        return teraz - datetime.timedelta(days=1) <= self.pub_data <= teraz

    opublikowane_ostatnio.admin_order_field = 'pub_data'
    opublikowane_ostatnio.boolean = True
    opublikowane_ostatnio.short_description = 'Opublikowane ostatnio?'

    def ma_odpowiedzi(self):
        return self.odpowiedz_set.all().count()


    class Meta:
        ordering = ['pub_data']
        verbose_name_plural = "pytania"


class Odpowiedz(models.Model):
    pytanie = models.ForeignKey(Pytanie, on_delete=models.CASCADE)
    wybor_tekst = models.CharField("treść odpowiedzi", max_length=200)
    glosy = models.IntegerField(default=0)

    def __str__(self):
        return self.wybor_tekst


    class Meta:
        verbose_name_plural = "odpowiedzi"