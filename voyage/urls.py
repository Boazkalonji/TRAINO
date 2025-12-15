from django.urls import path

from .views import lire_voyage,creation_voyage,modifier_voyage,delete_voyage,details_voyage

app_name = 'voyage'

urlpatterns = [


    path('lire_voyage', lire_voyage , name = 'lire_voyage'),
    path('creation_voyage',creation_voyage.as_view(), name = 'creation_voyage'),
    path('modifier_voyage/<int:id>/<str:slug>',modifier_voyage.as_view(), name = 'modifier_voyage'),
    path('delete_voyage/<int:id>/<str:slug>',delete_voyage, name = 'delete_voyage'),
    path('details_voyage/<int:id>/',details_voyage, name = 'details_voyage'),


]
