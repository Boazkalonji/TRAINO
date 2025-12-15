from django.urls import path
from .views import Reservation_paiement,scannage,confirmation_reservation_paiement,lire_reservation_paiement,Rapport_journalier_cash_mobile,Rapport_journalier_cash,telecharger_qrcode,scannage_verifiaction_paiement,rapport_jour_cash,rapport_jour_cash_mobile,telecharger_ticket

app_name = 'reservation_paiement'

urlpatterns = [

    
    path('reservation_paiement',Reservation_paiement.as_view(), name = 'reservation_paiement'),
    path('confirmation_reservation_paiement/<int:id_paiement>',confirmation_reservation_paiement, name = 'confirmation_reservation_paiement'),
    path('rapport_journalier_cash', Rapport_journalier_cash.as_view(), name = 'rapport_journalier_cash'),
    path('rapport_journalier_cash_mobile', Rapport_journalier_cash_mobile.as_view(), name = 'rapport_journalier_cash_mobile'),
    path('telecharger_qrcode/<str:numero_billet>/', telecharger_qrcode, name='telecharger_qrcode'),
    path('scannage', scannage, name='scannage'), 
    path('rapport_jour_cash', rapport_jour_cash, name='rapport_jour_cash'),
    path('rapport_jour_cash_mobile', rapport_jour_cash_mobile, name='rapport_jour_cash_mobile'),  
    path('scannage_verifiaction_paiement', scannage_verifiaction_paiement, name='scannage_verifiaction_paiement'),
    path('telecharger_ticket', telecharger_ticket, name='telecharger_ticket'), 





]
