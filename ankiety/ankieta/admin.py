from django.contrib import admin

# Register your models here.
from .models import Pytanie, Odpowiedz

class PytanieAdmin(admin.ModelAdmin):
    fields = ['pub_data', 'pytanie_tekst']

class OdpowiedzAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Pytanie i odpowiedź', {'fields': ['pytanie']}),
        (None, {'fields': ['wybor_tekst']}),
        ('Oddane głosy', {'fields': ['glosy']}),
    ]

admin.site.register(Pytanie, PytanieAdmin)
admin.site.register(Odpowiedz, OdpowiedzAdmin)