from django.db import models

class Pytanie(models.Model):
    pytanie_tekst = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data publikacji')

class Odpowiedz(models.Model):
    pytanie = models.ForeignKey(Pytanie, on_delete=models.CASCADE)
    wybor_tekst = models.CharField(max_length=200)
    glosy = models.IntegerField(default=0)