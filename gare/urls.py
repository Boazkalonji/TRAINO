from django.urls import path

from .views import lire_gare,creation_gare,modifier_gare,delete_gare,details_gare

app_name = 'gare'

urlpatterns = [


    path('lire_gare', lire_gare , name = 'lire_gare'),
    path('creation_gare',creation_gare.as_view(), name = 'creation_gare'),
    path('modifier_gare/<int:id>/<str:slug>',modifier_gare.as_view(), name = 'modifier_gare'),
    path('delete_gare/<int:id>/<str:slug>',delete_gare, name = 'delete_gare'),
    path('details_gare/<int:id>/',details_gare, name = 'details_gare'),


]
