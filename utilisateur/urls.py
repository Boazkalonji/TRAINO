from django.urls import path
from utilisateur.views import logout_compte,login_comptes,creation_comptes,profil,modifier_compte,supprimer_compte,confirmation_compte
from django_registration.backends.activation.views import ActivationView



app_name = 'utilisateur'




urlpatterns = [



    path('creation_comptes',creation_comptes.as_view(), name = 'creation_comptes'),
    path('login_comptes',login_comptes.as_view(), name = 'login_comptes'),
    path('logout_compte',logout_compte.as_view(), name = 'logout_compte'),
    path('modifier_compte/<int:id>',modifier_compte.as_view(), name = 'modifier_compte'),
    path('supprimer_compte/<int:id>',supprimer_compte.as_view(), name = 'supprimer_compte'),
    path('profil',profil, name = 'profil'),
    path('confirmation_compte',confirmation_compte.as_view(), name = 'confirmation_compte'),


    path('activation_compte/<activation_key>/', ActivationView.as_view(
        template_name='utilisateur/comptes/operation_comptes/compte_activation.html'
    ), name='registration_activate'),
    



]
