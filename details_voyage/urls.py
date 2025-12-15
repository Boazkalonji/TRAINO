from django.urls import path

from .views import lire_details_voyage,creation_details_voyage,modifier_details_voyage,delete_details_voyage,details_details_voyage

app_name = 'details_voyage'

urlpatterns = [


    path('lire_details_voyage', lire_details_voyage , name = 'lire_details_voyage'),
    path('creation_details_voyage',creation_details_voyage.as_view(), name = 'creation_details_voyage'),
    path('modifier_details_voyage/<int:id>/<str:slug>',modifier_details_voyage.as_view(), name = 'modifier_details_voyage'),
    path('delete_details_voyage/<int:id>/<str:slug>',delete_details_voyage, name = 'delete_details_voyage'),
    path('details_details_voyage/<int:id>/',details_details_voyage, name = 'details_details_voyage'),


]
