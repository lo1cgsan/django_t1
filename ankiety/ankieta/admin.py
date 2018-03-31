from django.contrib import admin

# Register your models here.
from .models import Pytanie, Odpowiedz

admin.site.register(Pytanie)
admin.site.register(Odpowiedz)