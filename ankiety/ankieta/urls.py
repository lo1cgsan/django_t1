from django.urls import path

from . import views

app_name = 'ankieta'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.SzczegolyView.as_view(), name='szczegoly'),
    path('<int:pk>/wyniki', views.WynikiView.as_view(), name='wyniki'),
    path('<int:pytanie_id>/glos', views.glos, name='glos'),
]