from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO 





def send_confirmation_email(user, paiement, qr_code_buffer):
    # 1. Contexte de l'e-mail
    context = {
        'username': user.username,
        'date_reservation': paiement.date_paiement, 
        'numero_billet': paiement.numero_billet,
        'montant': paiement.montant_paiement,
        'mode_paiement': paiement.id_mode_paiement.libelle_mode,
        'gare_depart' : paiement.id_tarification.id_details_voyage.id_gare_depart.libelle_gare,
        'gare_arrivee':paiement.id_tarification.id_details_voyage.id_gare_arrive.libelle_gare,
        'distance' : paiement.id_tarification.id_details_voyage.distance,
        'paiement':paiement,
       
    }


    html_content = render_to_string('reservation_paiement/send_confirmation_email.html', context)
    
    
    email = EmailMessage(
       
        f"✅ Confirmation de Réservation TRAINO - Billet N°{paiement.numero_billet}", 
    
        html_content,
        settings.EMAIL_HOST_USER, 
        [user.email], 
    )
    email.content_subtype = "html"  


    email.attach('qr_code_billet.png', qr_code_buffer.read(), 'image/png')
    
  
    try:
        email.send()
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")