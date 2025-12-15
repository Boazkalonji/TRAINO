from django.urls import path

from .views import lire_publication_avis,creation_publication_avis,modifier_publication_avis,delete_publication_avis,details_publication_avis,dernier_publication_avis,telecharger_dernier_publication_avis

app_name = 'publication_avis'

urlpatterns = [


    path('lire_publication_avis', lire_publication_avis , name = 'lire_publication_avis'),
    path('creation_publication_avis',creation_publication_avis.as_view(), name = 'creation_publication_avis'),
    path('modifier_publication_avis/<int:id>/<str:slug>',modifier_publication_avis.as_view(), name = 'modifier_publication_avis'),
    path('delete_publication_avis/<int:id>/<str:slug>',delete_publication_avis, name = 'delete_publication_avis'),
    path('details_publication_avis/<int:id>/',details_publication_avis, name = 'details_publication_avis'),
    path('dernier_publication_avis',dernier_publication_avis, name = 'dernier_publication_avis'),
    path('telecharger_dernier_publication_avis', telecharger_dernier_publication_avis , name = 'telecharger_dernier_publication_avis'),


]
