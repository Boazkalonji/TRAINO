from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from gare.models import Gare
from train.models import Train
from tarification.models import Tarification
from voyage.models import Voyage
from voiture.models import Voiture
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from details_voyage.models import Details_voyage
from django.db.models import Count,Sum
from .models import Paiement,Mode_paiement
from .generated_qrcode.genereted_qrcode import genereted_qrcode
from .generated_qrcode.send_confirmation_email import send_confirmation_email
from datetime import date
from django.http import FileResponse, Http404
from services.report_generator import generer_pdf_local
from services.generer_num_billet import generer_num_billet, extraire_initiales_gare
import os
from decimal import Decimal
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from services.report_generator import generer_pdf_local





@method_decorator(login_required, name='dispatch')
class Reservation_paiement(View):

    def get(self,request):

        context = {

        'gares' : Gare.objects.all().order_by('libelle_gare'),
        'trains': Train.objects.all(),
        

        }
        return render(request, 'reservation_paiement/reservation_paiement.html',context)

    def post(self,request):
        if request.method == 'POST':

            id_gare_depart = request.POST.get('id_gare_depart')
            id_gare_arrivee = request.POST.get('id_gare_arrivee')
            id_train = request.POST.get('id_train')

            designation_tarification = request.POST.get('tarification')
            
            nbr_adulte = request.POST.get('nbr_adulte')
            nbr_enfant = request.POST.get('nbr_enfant')


            
            nbr_adulte_int = int(nbr_adulte)
            if nbr_enfant != '':
                nbr_enfant_int = int(nbr_enfant)
            else:
                nbr_enfant_int = 0
   
            nbr_place_reserve = nbr_adulte_int + nbr_enfant_int
            if nbr_adulte_int <=0 :
                context = {'erreur': 'Veuillez saisir des nombres valides pour les passagers.'}
                return render(request, 'reservation_paiement/reservation_paiement.html', context)

            if id_gare_depart == id_gare_arrivee:
                context = {
                    'gares' : Gare.objects.all().order_by('libelle_gare'),
                    'trains': Train.objects.all(),
                    'erreur' : 'le point de depart et d\'arriver sont pareils'
                }
                return render(request,'reservation_paiement/reservation_paiement.html', context)






            try:
                
                tarification_obj = Tarification.objects.get(
                    id_details_voyage__id_gare_depart=id_gare_depart,
                    id_details_voyage__id_gare_arrive=id_gare_arrivee,
                    designation_tarififcation=designation_tarification
                )
                
                id_tarification = tarification_obj.pk
                prix_unitaire = tarification_obj.pu
                
              
                distance = tarification_obj.id_details_voyage.distance

            except Tarification.DoesNotExist:
                
                context = {
                    'erreur': f"Aucune tarification '{designation_tarification}' n'est définie pour ce trajet.",
                    'gares' : Gare.objects.all().order_by('libelle_gare'),
                    'trains': Train.objects.all()
                }
                return render(request, 'reservation_paiement/reservation_paiement.html', context)



                        
            mont_adulte = nbr_adulte_int * prix_unitaire
            mont_enfant = nbr_enfant_int * prix_unitaire
            mont_enfant = mont_enfant * 0.75 
            montant_paiement = mont_enfant + mont_adulte


            
           
            date_actuelle = datetime.now().date()
        
    
            try:

                voyages = Voyage.objects.filter(
                    id_train__pk=id_train,
                    date_depart__gte=date_actuelle
                ).order_by('-date_depart').first()

                if not voyages:
                
                    context = {'messages': "Aucun voyage futur trouvé pour ce train."}
                    return render(request, 'reservation_paiement/temps_depasser.html', context)

                date_depart_voyage = voyages.date_depart

            except Exception:
                context = {'erreur': "Erreur lors de la recherche du voyage."}
                return render(request, 'reservation_paiement/reservation_paiement.html', context)



            difference_temps = date_depart_voyage - date_actuelle


            if difference_temps <= timedelta(days=2):

            
                context = {
                    'messages': f"❌ **Réservation annulée.** La contrainte ONATRA exige que la réservation soit faite plus de 48 heures avant le départ. Le voyage du {date_depart_voyage.strftime('%d/%m/%Y')} n'est plus disponible.",
                }

                return render(request, 'reservation_paiement/temps_depasser.html', context)
            
            
            try:
            
                voitures_du_train = Voiture.objects.filter(
                    id_train__pk=id_train,
                    id_tarification__designation_tarififcation=designation_tarification
                )
                if not voitures_du_train.exists():
                
                    context = {'erreur': f"Aucune voiture/classe '{designation_tarification}' trouvée pour ce train."}
                    return render(request, 'reservation_paiement/reservation_paiement.html', context)

                capacite_agg = voitures_du_train.aggregate(
                    total_capacite=Sum('nombre_place')
                )
                capacite_totale = capacite_agg['total_capacite'] or 0 

            except Voiture.DoesNotExist:
                context = {'erreur': f"Aucune voiture/classe '{designation_tarification}' trouvée pour ce train."}
                return render(request, 'reservation_paiement/reservation_paiement.html', context)






















            places_reservees = Paiement.objects.filter(
                
                id_tarification__id_details_voyage__id_voyage=voyages.id, 
                id_tarification__designation_tarififcation=designation_tarification,
                statut=True 
            ).aggregate(
                
                total_places_prises=Sum('nombre_place_reserve') 
            )['total_places_prises'] or 0 

            
            
            places_restantes = capacite_totale - places_reservees

            if nbr_place_reserve <= places_restantes:
                
            
                utilisateur = request.user

                if utilisateur.is_authenticated:
                    id_user = utilisateur.id
                    email_user = str(utilisateur.email)

                    
                    nouveau_paiement = Paiement.objects.create(
                        id_user=User.objects.get(id=id_user), 
                        email_user = email_user,
                        id_tarification=Tarification.objects.get(id=id_tarification),
                        montant_paiement=montant_paiement,
          
                        nombre_place_reserve=nbr_place_reserve
                    )
                    
                    paiement_actuel = nouveau_paiement 

                    gare_depart = Gare.objects.get(id = id_gare_depart)
                    gare_arrivee = Gare.objects.get(id = id_gare_arrivee)



                    context = {
                        'id_paiement': paiement_actuel.id,
                        'message': "veuillez saisir vos données de paiement pour confirmer votre paiement",
                        'montant_paiement': montant_paiement,
                        'distance': distance, 
                        'mode_paiements': Mode_paiement.objects.all(),
                        'nbr_adulte_int' : nbr_adulte_int,
                        'nbr_enfant_int' : nbr_enfant_int,
                        'prix_unitaire' : prix_unitaire,
                        'gare_depart' : gare_depart.libelle_gare,
                        'gare_arrivee' : gare_arrivee.libelle_gare,
                        'mont_adulte' : mont_adulte,
                        'mont_enfant' : nbr_enfant_int * prix_unitaire,
                        'reduction' : nbr_enfant_int * prix_unitaire * 0.75
                    }

                    return render(request, 'reservation_paiement/confirmation_reservation_paiement.html', context)



            else:
                context = {
                    'gares' : Gare.objects.all().order_by('libelle_gare'),
                    'trains': Train.objects.all(),
                    'erreur' : f"Les nombre des place que vous voulais réservé est superieur aux place restante : {places_restantes}"
                }
                return render(request, 'reservation_paiement/reservation_paiement.html',context)

@login_required
def confirmation_reservation_paiement(request,id_paiement):

    if request.method == 'POST':

        id_paiement_post = request.POST.get('id_paiement') 
        id_mode_paiement = request.POST.get('id_mode_paiement')
        date_paiement = datetime.now().date() 
        montant_paiement = request.POST.get('montant_paiement')

        try:
           
            paiement = Paiement.objects.select_related(
                'id_tarification',
                'id_tarification__id_details_voyage',
                'id_tarification__id_details_voyage__id_gare_depart',
                'id_tarification__id_details_voyage__id_gare_arrive',
            ).get(id=id_paiement_post)

      
            details_voyage = paiement.id_tarification.id_details_voyage
            
           
            if not details_voyage:
                return HttpResponse('Erreur: Les détails du voyage ne sont pas liés correctement à la tarification.', status=500)

        except Paiement.DoesNotExist:
            return HttpResponse('Paiement non trouvé.', status=404)
        except Exception as e:
       
            print(f"Erreur lors de la récupération des données pour le billet : {e}")
            return HttpResponse('Erreur interne lors de la validation du paiement.', status=500)


   
        paiement.id_mode_paiement = Mode_paiement.objects.get(id=id_mode_paiement)
        paiement.date_paiement = date_paiement
        paiement.statut = True
        

        chaine_aleatoire = generer_num_billet(longueur=10) 
        
        
        libelle_depart = details_voyage.id_gare_depart.libelle_gare
        initiales_depart = extraire_initiales_gare(libelle_depart)
        
        libelle_arrivee = details_voyage.id_gare_arrive.libelle_gare
        initiales_arrivee = extraire_initiales_gare(libelle_arrivee)
        

        numero_billet_final = f"{initiales_depart}-{initiales_arrivee}-{chaine_aleatoire}" 

    
        valeur_qr_code = numero_billet_final
        
        qr_code_file = genereted_qrcode(valeur_qr_code)
        paiement.qr_code = qr_code_file 
        qr_code_buffer = qr_code_file 
        

        paiement.numero_billet = numero_billet_final
        paiement.save()

        send_confirmation_email(request.user, paiement, qr_code_buffer)

        return redirect('utilisateur:profil')
        
    else:   

        context = {}

        utilisateur = request.user        
        id_user = utilisateur.id

        paiement = Paiement.objects.get(id_user = id_user)

        context['id_paiement'] = paiement.id
        context['message'] = "veuillez saisir vos données de paiement pour confirmer votre paiement"
        context['montant_paiement'] = paiement.montant_paiement

        return render('reservation_paiement/confirmation_reservation_paiement.html',context)
    
@method_decorator(login_required, name='dispatch')
class lire_reservation_paiement(View):

    def get(self,request):

        return render(request, 'reservation_paiement/dashboard.html')

@method_decorator(login_required, name='dispatch')
class Rapport_journalier_cash(View):
    
    def get(self, request):
        
        date_str = request.GET.get('filter_date')
        

        date_rapport = date.today()
        filter_date_iso = date_rapport.isoformat()

        if date_str:
            try:
                
                date_rapport = datetime.strptime(date_str, '%Y-%m-%d').date()
                filter_date_iso = date_str
            except ValueError:
          
                context = {
                    'erreur' : f"Date de filtre invalide fournie: {date_str}. Utilisation de la date du jour."
                }
                return render(request, 'reservation_paiement/rapport_journalier_cash.html', context)
                

      
        try:
            
            mode_cash = Mode_paiement.objects.get(libelle_mode__iexact='cash')
        except Mode_paiement.DoesNotExist:
            context = {
                'erreur': "Le mode de paiement 'Cash' n'est pas configuré dans la base de données.",
                'date_rapport': date_rapport,
                'filter_date_iso': filter_date_iso,
            }
            return render(request, 'reservation_paiement/rapport_journalier_cash.html', context)

       
        try:
            ventes_cash = Paiement.objects.filter(
                date_paiement=date_rapport,  
                id_mode_paiement=mode_cash,
                statut=True
            ).select_related(
                'id_user',  
                'id_mode_paiement',  
                'id_tarification__id_details_voyage__id_gare_depart',
                'id_tarification__id_details_voyage__id_gare_arrive',
            ).order_by('-date_paiement')
            
       
            totaux = ventes_cash.aggregate(
                total_montant=Sum('montant_paiement'),
                total_places=Sum('nombre_place_reserve')
            )


            
        except Exception as e:
            context = {
                'erreur': f"Une erreur s'est produite lors de la récupération des données : {e}",
                'date_rapport': date_rapport,
                'filter_date_iso': filter_date_iso,
            }
         
            return render(request, 'reservation_paiement/rapport_journalier_cash.html', context)

        voyages =  Voyage.objects.aggregate(total = Count('id'))
        voyages = voyages['total']

        context = {
            'ventes': ventes_cash,
            'totaux': totaux,
            'date_rapport': date_rapport,
            'filter_date_iso': filter_date_iso, 
            'voyages' : voyages
        }
        
        return render(request, 'reservation_paiement/rapport_journalier_cash.html', context)
    
@login_required
def telecharger_qrcode(request, numero_billet):

    buffer = genereted_qrcode(numero_billet)
    

    response = HttpResponse(
        buffer.read(), 
        content_type='image/png' 
    )
    
   
    nom_file = f'qr_code_{numero_billet}.png'
    response['Content-Disposition'] = f'attachment; filename="{numero_billet}"'
    
    return response


@csrf_exempt
def scannage_verifiaction_paiement(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)
    
    try:
        data = json.loads(request.body)
        ticket_code = data.get('ticket_code')
        
        if not ticket_code:
            return JsonResponse({'status': 'error', 'message': 'Code de billet manquant.'}, status=400)

        try:
     
            billet = Paiement.objects.get(numero_billet=ticket_code)
            
           
            if billet.statut == False: 

                return JsonResponse({
                    'status': 'error', 
                    'message': 'Billet déjà utilisé ou expiré.',
                   
                    'passenger_name': f'Mr/Mme {billet.id_user.username} a déjà utilisé son billet.'
                })
            
            
            
            
            billet.statut = False  
            billet.save()          
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Ticket validé avec succès.',
                'passenger_name': f'Mr/Mme {billet.id_user.username} : Billet validé.'
            })
            
        except Paiement.DoesNotExist:
          
            return JsonResponse({
                'status': 'error', 
                'message': 'Code de billet invalide ou introuvable.'
            })

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Format de données invalide.'}, status=400)

@login_required
def scannage(request):
    """Affiche la page HTML du scanner."""
    return render(request, 'reservation_paiement/scannage.html')

@method_decorator(login_required, name='dispatch')
class Rapport_journalier_cash_mobile(View):
    
    def get(self, request):
        
        date_str = request.GET.get('filter_date')
        filter_mode = request.GET.get('filter_mode') 

    
        date_rapport = date.today()
        filter_date_iso = date_rapport.isoformat()
        
        erreur = None 

        if date_str:
            try:
                
                date_rapport = datetime.strptime(date_str, '%Y-%m-%d').date()
                filter_date_iso = date_str
            except ValueError:
                
                erreur = f"Date de filtre invalide fournie: {date_str}. Utilisation de la date du jour."
                

        modes_a_filtrer = []
        mode_cash = None
        mode_mobile = None
        
        try:
            mode_cash = Mode_paiement.objects.get(libelle_mode__iexact='cash')
            mode_mobile = Mode_paiement.objects.get(libelle_mode__iexact='mobile money')
            
        
            if not filter_mode or filter_mode == 'tous':
                modes_a_filtrer = [mode_cash.id, mode_mobile.id]
            elif filter_mode == 'cash':
                modes_a_filtrer = [mode_cash.id]
            elif filter_mode == 'mobile':
                modes_a_filtrer = [mode_mobile.id]
            
        except Mode_paiement.DoesNotExist as e:
            mode_libelle = 'Cash' if 'cash' in str(e).lower() else 'Mobile Money'
            context = {
                'erreur': f"Erreur de configuration: Le mode de paiement '{mode_libelle}' n'est pas configuré dans la base de données.",
                'date_rapport': date_rapport,
                'filter_date_iso': filter_date_iso,
                'filter_mode': filter_mode # Ajout du mode au contexte
            }
            return render(request, 'reservation_paiement/rapport_journalier_cash_mobile.html', context)

        # 3. Initialisation des totaux
        ventes_filtrees = []
        totaux_cash = {
            'total_montant': Decimal(0),
            'total_places': 0
        }
        totaux_mobile = {
            'total_montant': Decimal(0),
            'total_places': 0
        }
        totaux_globaux = {
            'total_montant': Decimal(0),
            'total_places': 0
        }
        
        try:

            ventes_globales = Paiement.objects.filter(
                date_paiement=date_rapport, 
                id_mode_paiement__in=modes_a_filtrer,
                statut=True
            ).select_related(
                'id_user',  
                'id_mode_paiement',  
                'id_tarification__id_details_voyage__id_gare_depart',
                'id_tarification__id_details_voyage__id_gare_arrive',
            ).order_by('-date_paiement')

            if  mode_cash:
                 cash_agg = Paiement.objects.filter(
                    date_paiement=date_rapport, 
                    id_mode_paiement=mode_cash,
                    statut=True
                 ).aggregate(
                    montant=Sum('montant_paiement'),
                    places=Sum('nombre_place_reserve')
                 )
                 totaux_cash['total_montant'] = cash_agg.get('montant') or Decimal(0.00)
                 totaux_cash['total_places'] = cash_agg.get('places') or 0
            
            if mode_mobile:
                mobile_agg = Paiement.objects.filter(
                    date_paiement=date_rapport, 
                    id_mode_paiement=mode_mobile,
                    statut=True
                 ).aggregate(
                    montant=Sum('montant_paiement'),
                    places=Sum('nombre_place_reserve')
                 )
                totaux_mobile['total_montant'] = mobile_agg.get('montant') or Decimal(0.00)
                totaux_mobile['total_places'] = mobile_agg.get('places') or 0
            
        
            totaux_globaux['total_montant'] = totaux_cash['total_montant'] + totaux_mobile['total_montant']
            totaux_globaux['total_places'] = totaux_cash['total_places'] + totaux_mobile['total_places']

            ventes_filtrees = ventes_globales 
            
        except Exception as e:
            erreur = f"Une erreur s'est produite lors de la récupération des données : {e}"

        try:
            voyages_count = Voyage.objects.aggregate(total = Count('id'))
            voyages = voyages_count['total']
        except Exception:
            voyages = 0

        
        context = {
            'ventes': ventes_filtrees,
            'totaux_cash': totaux_cash,
            'totaux_mobile': totaux_mobile,
            'totaux_globaux': totaux_globaux,
            'date_rapport': date_rapport,
            'filter_date_iso': filter_date_iso, 
            'filter_mode': filter_mode, 
            'voyages' : voyages,
            'erreur': erreur,
        }
        
        return render(request, 'reservation_paiement/rapport_journalier_cash_mobile.html', context)

@login_required
def rapport_jour_cash(request): 
    

    DB_CONFIG = {
        'HOST': '127.0.0.1', 
        'USER': 'postgres', 
        'PASS': 'kalonji082', 
        'NAME': 'TRAINO',
        'PORT': '5432'
    }
    
    # B. Configuration du rapport
    JASPER_FILE = 'rapport_jour_cash.jrxml' # Votre fichier .jasper
    #JASPER_FILE = 'rapport_jour_cash.jasper' # Votre fichier .jasper
    PDF_OUTPUT = 'rapport_jour_cash.pdf'
    
    # C. Les paramètres sont nuls ou omis
    today_date_str = date.today().strftime('%d-%m-%Y')
    report_params = {
        'P_CURRENT_DATE_STRING': today_date_str 
    }

    # 1. Génération du PDF
    pdf_path = generer_pdf_local(
        jasper_filename=JASPER_FILE,
        output_filename=PDF_OUTPUT,
        db_config=DB_CONFIG,
        parameters=report_params 
    )

    # ... (Le reste de la logique pour servir le fichier est inchangé)
    if pdf_path:
        try:
            # 1. Lire tout le contenu du fichier dans la mémoire
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
                
            # 2. Supprimer le fichier TANT QU'IL N'EST PAS OUVERT par un autre processus
            os.remove(pdf_path)
            
            # 3. Servir la réponse à partir du contenu en mémoire (utiliser HttpResponse)
            from django.http import HttpResponse # Assurez-vous d'importer HttpResponse
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{PDF_OUTPUT}"'
            return response

        except Exception as e:
            # S'il y a une erreur dans le traitement ci-dessus, assurez-vous que le fichier est nettoyé
            if os.path.exists(pdf_path):
                 os.remove(pdf_path) # Nettoyage si possible
            
            # Afficher ou enregistrer l'erreur, puis renvoyer le 404
            print(f"Erreur de traitement du PDF : {e}")
            raise Http404("Échec de la génération du rapport.")

    else:
        raise Http404("Échec de la génération du rapport.")

@login_required
def rapport_jour_cash_mobile(request): 
    

    DB_CONFIG = {
        'HOST': '127.0.0.1', 
        'USER': 'postgres', 
        'PASS': 'kalonji082', 
        'NAME': 'TRAINO',
        'PORT': '5432'
    }
    
    # B. Configuration du rapport
    JASPER_FILE = 'rapport_jour_cash_mobile.jrxml' # Votre fichier .jasper
    #JASPER_FILE = 'rapport_jour_cash.jasper' # Votre fichier .jasper
    PDF_OUTPUT = 'rapport_jour_cash_mobile.pdf'
    
    # C. Les paramètres sont nuls ou omis
    today_date_str = date.today().strftime('%d-%m-%Y')
    report_params = {
        'P_CURRENT_DATE_STRING': today_date_str 
    }

    # 1. Génération du PDF
    pdf_path = generer_pdf_local(
        jasper_filename=JASPER_FILE,
        output_filename=PDF_OUTPUT,
        db_config=DB_CONFIG,
        parameters=report_params 
    )

    # ... (Le reste de la logique pour servir le fichier est inchangé)
    if pdf_path:
        try:
            # 1. Lire tout le contenu du fichier dans la mémoire
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
                
            # 2. Supprimer le fichier TANT QU'IL N'EST PAS OUVERT par un autre processus
            os.remove(pdf_path)
            
            # 3. Servir la réponse à partir du contenu en mémoire (utiliser HttpResponse)
            from django.http import HttpResponse # Assurez-vous d'importer HttpResponse
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{PDF_OUTPUT}"'
            return response

        except Exception as e:
            # S'il y a une erreur dans le traitement ci-dessus, assurez-vous que le fichier est nettoyé
            if os.path.exists(pdf_path):
                 os.remove(pdf_path) # Nettoyage si possible
            
            # Afficher ou enregistrer l'erreur, puis renvoyer le 404
            print(f"Erreur de traitement du PDF : {e}")
            raise Http404("Échec de la génération du rapport.")

    else:
        raise Http404("Échec de la génération du rapport.")

@login_required
def telecharger_ticket(request): 
    

    DB_CONFIG = {
        'HOST': '127.0.0.1', 
        'USER': 'postgres', 
        'PASS': 'kalonji082', 
        'NAME': 'TRAINO',
        'PORT': '5432'
    }


    
    
    EMAIL_USER = request.user.email
    NOM_USER = request.user.username
    MEDIA_ROOT_PATH = settings.MEDIA_ROOT


    print(f'mes recuperation : {EMAIL_USER} - {NOM_USER} - {MEDIA_ROOT_PATH}')

    
    JASPER_FILE = 'telecharger_ticket_new.jrxml' 
    PDF_OUTPUT = f'ticket_client_{NOM_USER}.pdf'

    report_params = {
        'P_EMAIL_USER': str(EMAIL_USER),
        #'P_MEDIA_ROOT': str(MEDIA_ROOT_PATH) + os.sep
    }



    # 1. Génération du PDF
    pdf_path = generer_pdf_local(
        jasper_filename=JASPER_FILE,
        output_filename=PDF_OUTPUT,
        db_config=DB_CONFIG,
        parameters=report_params 
    )

    # ... (Le reste de la logique pour servir le fichier est inchangé)
    if pdf_path:
        try:
            # 1. Lire tout le contenu du fichier dans la mémoire
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
                
            # 2. Supprimer le fichier TANT QU'IL N'EST PAS OUVERT par un autre processus
            os.remove(pdf_path)
            
            # 3. Servir la réponse à partir du contenu en mémoire (utiliser HttpResponse)
            from django.http import HttpResponse # Assurez-vous d'importer HttpResponse
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{PDF_OUTPUT}"'
            return response

        except Exception as e:
            # S'il y a une erreur dans le traitement ci-dessus, assurez-vous que le fichier est nettoyé
            if os.path.exists(pdf_path):
                 os.remove(pdf_path) # Nettoyage si possible
            
            # Afficher ou enregistrer l'erreur, puis renvoyer le 404
            print(f"Erreur de traitement du PDF : {e}")
            raise Http404("Échec de la génération du rapport.")

    else:
        raise Http404("Échec de la génération du rapport.")