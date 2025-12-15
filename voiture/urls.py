from django.urls import path

from .views import lire_voiture,creation_voiture,modifier_voiture,delete_voiture,details_voiture

app_name = 'voiture'

urlpatterns = [


    path('lire_voiture', lire_voiture , name = 'lire_voiture'),
    path('creation_voiture',creation_voiture.as_view(), name = 'creation_voiture'),
    path('modifier_voiture/<int:id>/<str:slug>',modifier_voiture.as_view(), name = 'modifier_voiture'),
    path('delete_voiture/<int:id>/<str:slug>',delete_voiture, name = 'delete_voiture'),
    path('details_voiture/<int:id>/',details_voiture, name = 'details_voiture'),


]
