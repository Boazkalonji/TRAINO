from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.views import View
from django.shortcuts import render
from .models import Publication_avis,Pubilaction_tarification
from datetime import datetime
from tarification.models import Tarification
from django.db.models import Max
from services.report_generator import generer_pdf_local,render_to_pdf
import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


import os
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import Publication_avis 
from tarification.models import Tarification 





@method_decorator(login_required, name='dispatch')
class   creation_publication_avis(View):


    def get(self,request):
        return render(request,'publication_avis/publication_avis_form.html')




    def post(self,request):
        if request.method == 'POST':

            reference_avis = request.POST.get('reference_avis')
            titre_avis = request.POST.get('titre_avis')
            message_avis = request.POST.get('message_avis')
            date_avis = request.POST.get('date_avis')
            consigne_avis = request.POST.get('consigne_avis')
            format_date = "%Y-%m-%d"
            obje_date_avis = datetime.strptime(date_avis, format_date)
            obje_date_avis = obje_date_avis.date()
            

            




            if reference_avis =='' or titre_avis == '' or message_avis == '' or obje_date_avis < datetime.now().date():

                context = {
                    'erreur' : 'veuillez revoir vos informations il y a une erreur'
                }
                return render(request,'publication_avis/publication_avis_form.html', context)
            else:
                
                nouvelle_avis= Publication_avis.objects.create(
                    reference_avis = f'avis au pluc n° {reference_avis}/ONATRA-DG/DCO/2025',
                    titre_avis = titre_avis,
                    message_avis = message_avis,
                    date_avis = obje_date_avis,
                    consigne_avis = consigne_avis

                )

                return redirect('publication_avis:lire_publication_avis')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'publication_avis/publication_avis_form.html')

@method_decorator(login_required, name='dispatch')
class   modifier_publication_avis(View):





    def get(self,request,id,slug):
        context  = {

            'publication_avis' : get_object_or_404(Publication_avis,id = id),
        }
        return render(request,'publication_avis/modifier_publication_avis.html', context)


    def post(self,request,id,slug):

        if request.method == 'POST':

            reference_avis = request.POST.get('reference_avis')
            titre_avis = request.POST.get('titre_avis')
            message_avis = request.POST.get('message_avis')
            date_avis = request.POST.get('date_avis')
            consigne_avis = request.POST.get('consigne_avis')
            format_date = "%Y-%m-%d"
            obje_date_avis = datetime.strptime(date_avis, format_date)
            obje_date_avis = obje_date_avis.date()
            

            
            publication_avis = Publication_avis.objects.get(id=id)

            context  = {

                'erreur' : "la publication n'existe pas , donc impossible de modifier"
            }
            if  publication_avis is not None:
                publication_avis.reference_avis = f'avis au pluc n° {reference_avis}/ONATRA-DG/DCO/2025'
                publication_avis.titre_avis =titre_avis
                publication_avis.message_avis = message_avis
                publication_avis.date_avis =obje_date_avis
                publication_avis.consigne_avis = consigne_avis

                publication_avis.save()
                return redirect('publication_avis:lire_publication_avis')
            
            return render(request,'publication_avis/dashbord_publication_avis.html', context)
        else:
            context  = {

                'erreur' : "le formulaire n'est pas valide"
            }
            return render(request,'publication_avis/modifier_publication_avis.html', context)   

@login_required
def lire_publication_avis(request):
    context = {

        'publication_avis' : Publication_avis.objects.all(),
        'total_compt' : Publication_avis.objects.count(),
    } 
    return render(request, 'publication_avis/dashbord_publication_avis.html', context)

@login_required
def delete_publication_avis(request,id, slug):
    publication_avis = Publication_avis.objects.get(pk = id)
    publication_avis.delete()
    return redirect('publication_avis:lire_publication_avis')

@login_required
def details_publication_avis(request, id):

    tarification_avis_pu = Tarification.objects.values(
        'designation_tarififcation'
    ).annotate(
        pu_le_plus_eleve = Max('pu')
        ).order_by('-pu_le_plus_eleve') 
    context = {

        'publication_avis' : Publication_avis.objects.get(id = id),
        'tarification_max' : tarification_avis_pu


    } 
    return render(request, 'publication_avis/details_publication_avis.html', context)

@login_required
def dernier_publication_avis(request):
    template_name = 'publication_avis/dernier_publication_avis.html'

  
    tarification_avis_pu = Tarification.objects.values(
        'designation_tarififcation'
    ).annotate(
        pu_le_plus_eleve = Max('pu')
    ).order_by('-pu_le_plus_eleve') 
    

    publication_avis = Publication_avis.objects.order_by('-id').first()
    
    context = {
        'tarification_max' : tarification_avis_pu,
    }

    if publication_avis:

        context['publication_avis'] = publication_avis
    else:
        
        context['message_publication_vide'] = "Pas de publication pour le moment."
        
    return render(request, template_name, context)



"""
@login_required
def telecharger_dernier_publication_avis(request): 
    

    DB_CONFIG = {
        'HOST': '127.0.0.1', 
        'USER': 'postgres', 
        'PASS': 'kalonji082', 
        'NAME': 'TRAINO',
        'PORT': '5432'
    }
    

    


    # B. Configuration du rapport
    JASPER_FILE = 'telecharger_dernier_publication_avis.jrxml' # Votre fichier .jasper
    #JASPER_FILE = 'telecharger_dernier_publication_avis.jasper' # Votre fichier .jasper
    PDF_OUTPUT = f'telecharger_dernier_publication_avis.pdf'

    report_params = None

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

"""












@login_required
def telecharger_dernier_publication_avis(request): 
    

    publication_avis = Publication_avis.objects.order_by('-id').first()

    if not publication_avis:
      
        raise Http404("Aucune publication disponible pour le téléchargement.")

    
    tarification_avis_pu = Tarification.objects.values(
        'designation_tarififcation'
    ).annotate(
        pu_le_plus_eleve = Max('pu')
    ).order_by('-pu_le_plus_eleve') 
    
 
    context = {
        'publication_avis': publication_avis,
        'tarification_max': tarification_avis_pu,
        
    }
    

    template_src = 'publication_avis/dernier_publication_avis_pdf_render.html' 
   


    pdf_data = render_to_pdf(template_src, context)
    
    if pdf_data:
        PDF_OUTPUT = f'avis_{publication_avis.reference_avis}_{publication_avis.date_avis}.pdf'
        
   
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{PDF_OUTPUT}"'
        return response

    else:
    
        raise Http404("Échec de la génération du rapport PDF.")