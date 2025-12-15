from django.urls import path
from .views import lire_categorie,creation_categorie,modifier_categorie,delete_categorie,details_categorie



app_name = 'traino_materiel'

urlpatterns = [

    #debut Gestion categorie

    path('lire_categorie', lire_categorie , name = 'lire_categorie'),
    path('creation_categorie',creation_categorie.as_view(), name = 'creation_categorie'),
    path('modifier_categorie/<int:id>/<str:slug>',modifier_categorie.as_view(), name = 'modifier_categorie'),
    path('delete_categorie/<int:id>/<str:slug>',delete_categorie, name = 'delete_categorie'),
    path('details_categorie/<int:id>/',details_categorie, name = 'details_categorie'),

    #fin gestion categorie




]
