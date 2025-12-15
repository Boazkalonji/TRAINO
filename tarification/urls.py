from django.urls import path
from .views import lire_tarification,creation_tarification,modifier_tarification,delete_tarification,details_tarification,grille_tarifaire



app_name = 'tarification'

urlpatterns = [

    

    path('lire_tarification', lire_tarification , name = 'lire_tarification'),
    path('creation_tarification',creation_tarification.as_view(), name = 'creation_tarification'),
    path('modifier_tarification/<int:id>/<str:slug>',modifier_tarification.as_view(), name = 'modifier_tarification'),
    path('delete_tarification/<int:id>',delete_tarification, name = 'delete_tarification'),
    path('details_tarification/<int:id>/<str:slug>',details_tarification, name = 'details_tarification'),
    path('grille_tarifaire',grille_tarifaire, name = 'grille_tarifaire'),

    




]
