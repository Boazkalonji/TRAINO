from django.urls import path

from .views import lire_train,creation_train,modifier_train,delete_train,details_train

app_name = 'train'

urlpatterns = [


    path('lire_train', lire_train , name = 'lire_train'),
    path('creation_train',creation_train.as_view(), name = 'creation_train'),
    path('modifier_train/<int:id>/<str:slug>',modifier_train.as_view(), name = 'modifier_train'),
    path('delete_train/<int:id>/<str:slug>',delete_train, name = 'delete_train'),
    path('details_train/<int:id>/',details_train, name = 'details_train'),


]
