from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.views import View
from .models import Tarification
from details_voyage.models import Details_voyage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator





@method_decorator(login_required, name='dispatch')
class   creation_tarification(View):


    def get(self,request):
        context = {'details_voyages' :  Details_voyage.objects.all(),
   
        }
        return render(request,'tarification/tarification.html',context)




    def post(self,request):
        if request.method == 'POST':

            id_details_voyage = request.POST.get('id_details_voyage')

            premium = request.POST.get('premium')
            pu_premium = request.POST.get('pu_premium')

            luxe = request.POST.get('luxe')
            pu_luxe = request.POST.get('pu_luxe')

            premiere_classe = request.POST.get('premiere_classe')
            pu_premiere_classe = request.POST.get('pu_premiere_classe')


     


            if id_details_voyage =='' or pu_premium == '' or pu_luxe == '' or pu_premiere_classe == '':
                return render(request,'tarification/tarification.html')
            else:
                
                Tarification.objects.create(
                    id_details_voyage=Details_voyage.objects.get(id = id_details_voyage), 
                    pu = int(pu_premiere_classe),
                    designation_tarififcation = premiere_classe
                )



                Tarification.objects.create(
                    id_details_voyage=Details_voyage.objects.get(id = id_details_voyage), 
                    pu = int(pu_luxe),
                    designation_tarififcation = luxe
                )


                Tarification.objects.create(
                    id_details_voyage = Details_voyage.objects.get(id = id_details_voyage), 
                    pu = int(pu_premium),
                    designation_tarififcation = premium
                )

                return redirect('tarification:lire_tarification')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'tarification/tarification.html')

@login_required
def delete_tarification(request, id):

    details_voyage_id = id 
    
  
    if Tarification.objects.filter(id_details_voyage_id=details_voyage_id).exists():
    
        Tarification.objects.filter(id_details_voyage_id=details_voyage_id).delete()
    else:
  
        print(f"Aucune tarification trouvée pour le trajet d'ont  l'id est : {details_voyage_id}")

    return redirect('tarification:lire_tarification')

@login_required
def grille_tarifaire(request):
    

    tarifications_data = Tarification.objects.filter(
        designation_tarififcation__in=['1èreclasse', 'premium', 'luxe']

    ).select_related(

        'id_details_voyage__id_gare_depart', 
        'id_details_voyage__id_gare_arrive'
    ).order_by('id_details_voyage__distance')

    tableau_data = {}
    
    
    for tarif in tarifications_data:
        voyage_details = tarif.id_details_voyage
        details_id = voyage_details.id
        
        if details_id not in tableau_data:
           
            tableau_data[details_id] = {
                'gare_depart': voyage_details.id_gare_depart.libelle_gare, # <- Votre syntaxe propre
                'gare_arrivee': voyage_details.id_gare_arrive.libelle_gare, # <- Votre syntaxe propre
                'distance': voyage_details.distance,
            }
        
        tableau_data[details_id][tarif.designation_tarififcation] = tarif.pu
        
    context = {
        'lignes_tableau': tableau_data.values(), 
        'total_compt': Tarification.objects.count(),
    }
    
    return render(request, 'tarification/grille_tarifaire.html', context)

@method_decorator(login_required, name='dispatch')
class  modifier_tarification(View):



    def get(self, request, id, slug):
        

        details_voyage_obj = get_object_or_404(Details_voyage, id=id)
        details_voyage_id = details_voyage_obj.id

        tarifs_trajet = Tarification.objects.filter(id_details_voyage = details_voyage_id)
        

        if not tarifs_trajet.exists():
            raise Http404("Aucun tarif trouvé pour ce trajet ID.")

        context = {
            'details_voyages': Details_voyage.objects.all(),
            'details_voyage_id' : details_voyage_id,
            'tarifs': {},
        }


        for tarif in tarifs_trajet:
             if tarif.designation_tarififcation == '1èreclasse':
                 context['tarifs']['premiere_classe'] = tarif.pu
             elif tarif.designation_tarififcation == 'luxe':
                 context['tarifs']['luxe'] = tarif.pu
             elif tarif.designation_tarififcation == 'premium': 
                 context['tarifs']['premium'] = tarif.pu
                 
        return render(request, 'tarification/modifier_tarification.html', context)


    def post(self, request, id, slug):


        tarification_initiale = get_object_or_404(Tarification, id=id)
        details_voyage_id = tarification_initiale.id_details_voyage.id


        pu_premium = request.POST.get('pu_premium')
        pu_luxe = request.POST.get('pu_luxe')
        pu_premiere_classe = request.POST.get('pu_premiere_classe')

        if tarification_initiale != None and details_voyage_id != None:

            Tarification.objects.filter(
                id_details_voyage_id=details_voyage_id,
                designation_tarififcation='1èreclasse'
            ).update(pu=int(pu_premiere_classe))


            Tarification.objects.filter(
                id_details_voyage_id=details_voyage_id,
                designation_tarififcation='luxe'
            ).update(pu=int(pu_luxe))


            Tarification.objects.filter(
                id_details_voyage_id=details_voyage_id,
                designation_tarififcation='premium'
            ).update(pu=int(pu_premium))

    
            return redirect('tarification:lire_tarification')

        context = {
            'erreur' : 'veuillez revoir les informations saisie (modification échouée)'
        }
        return render(request, 'tarification/modifier_tarification.html', context)

@login_required
def lire_tarification(request):
    
    details_voyages = Details_voyage.objects.all().select_related(
        'id_voyage', 
        'id_gare_depart', 
        'id_gare_arrive'
    ).order_by('id_voyage', 'id_gare_depart') 





    
    tarifications_data = Tarification.objects.filter(
        designation_tarififcation__in=['1èreclasse', 'premium', 'luxe']

    ).select_related(

        'id_details_voyage__id_gare_depart', 
        'id_details_voyage__id_gare_arrive'
    ).order_by('id_details_voyage__distance')

    tableau_data = {}
    
    
    for tarif in tarifications_data:
        voyage_details = tarif.id_details_voyage
        details_id = voyage_details.id
        
        if details_id not in tableau_data:
           
            tableau_data[details_id] = {
                'id' : details_id,
                'gare_depart': voyage_details.id_gare_depart.libelle_gare, 
                'gare_arrivee': voyage_details.id_gare_arrive.libelle_gare, 
                'distance': voyage_details.distance,
                'slug': voyage_details.slug
            }
        
        tableau_data[details_id][tarif.designation_tarififcation] = tarif.pu
        
    context = {
        'lignes_tableau': tableau_data.values(), 
        'total_compt': Tarification.objects.count(),
        'details_voyages': details_voyages, 
    }





    return render(request, 'tarification/dashbord_tarification.html', context)

@login_required
def details_tarification(request, id, slug):

    details_voyage_obj = get_object_or_404(Details_voyage, id=id, slug=slug)
    details_voyage_id = details_voyage_obj.id

    tarifs_trajet_qs = Tarification.objects.filter(
        id_details_voyage_id=details_voyage_id,
        designation_tarififcation__in=['1èreclasse', 'premium', 'luxe']
    )
    
  
    tarifs_dict = {}
    for tarif in tarifs_trajet_qs:
      
        if tarif.designation_tarififcation == '1èreclasse':
            tarifs_dict['premiereclasse'] = tarif.pu
        elif tarif.designation_tarififcation == 'premium':
            tarifs_dict['Premium'] = tarif.pu
        elif tarif.designation_tarififcation == 'luxe':
            tarifs_dict['Luxe'] = tarif.pu

    context = {
        'details_voyage': details_voyage_obj,
        'tarifs': tarifs_dict,
    }
    
    return render(request, 'tarification/details_tarification.html', context)
    



