from django.contrib import admin

# Register your models here.
from .models import Pytanie, Odpowiedz

# class OdpowiedzInline(admin.StackedInline):
class OdpowiedzInline(admin.TabularInline):
    model = Odpowiedz
    extra = 3


class PytanieAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['pytanie_tekst']}),
        ('Data dodania', {'fields': ['pub_data'], 'classes': ['collapse']}),
    ]
    inlines = [OdpowiedzInline]
    # definicja zawartości listy obiektów
    list_display = ('pytanie_tekst', 'pub_data', 'opublikowane_ostatnio')
    # definicja pól wg których można filtrować obiekty
    list_filter = ['pub_data']
    # pola wg których można wyszukiwać
    search_fields = ['pytanie_tekst']
#    fields = ['pub_data', 'pytanie_tekst']


class OdpowiedzAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Pytanie i odpowiedź', {'fields': ['pytanie']}),
        (None, {'fields': ['wybor_tekst']}),
        ('Oddane głosy', {'fields': ['glosy']}),
    ]


admin.site.register(Pytanie, PytanieAdmin)
admin.site.register(Odpowiedz, OdpowiedzAdmin)