from django.contrib import admin

# Register your models here.
from .models import Pytanie, Odpowiedz

class PytanieAdmin(admin.ModelAdmin):
    fields = ['pub_data', 'pytanie_tekst']

admin.site.register(Pytanie, PytanieAdmin)
admin.site.register(Odpowiedz)