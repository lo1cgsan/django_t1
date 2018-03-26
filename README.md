# Ankiety

Przykładowa aplikacja z tutoriala Django:

https://docs.djangoproject.com/pl/2.0/intro/tutorial01/


# Aplikacja wykorzystuje

- Django 2.0.3 (sprawdź poleceniem `python -m django -version`)

# Przygotowanie środowiska wirtualnego:
    
    ~$ git clone https://github.com/lo1cgsan/django_t1.git
    ~$ cd django_t1
    django_t1$ virtualenv -p python3.6 .pve
    django_t1$ source .pve/bin/activate
    django_t1$ pip install -r requirements.txt

Serwer uruchamiamy po aktywowaniu środowiska wirtualnego
(poleceniem: `source .pve/bin/activate`), w katalogu `malybar`:

    ~/djang_t1/ankiety$ python manage.py runserver
