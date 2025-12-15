from django.shortcuts import render,redirect
from django.views import View
from details_voyage.models import Details_voyage
from publication_avis.models import Publication_avis
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class Index(View):


    def get(self,request):

        publications_list = Publication_avis.objects.all().order_by('-date_avis')[:8]
    
    
        premiere_ligne = publications_list[:4]
        deuxieme_ligne = publications_list[4:8] 

        context = {
            'details_voyage': Details_voyage.objects.all(),
            'premiere_ligne_pub': premiere_ligne,
            'deuxieme_ligne_pub': deuxieme_ligne,
            'details_voyage_recherche' : Details_voyage.objects.all(),
        }

        return render(request, 'front/index.html', context)
    
    def post(self,request):
            
        if request.method == 'POST':

            recherche = request.POST.get('recherche')

            details_voyage_recherches = Details_voyage.objects.filter(
                id_gare_depart__libelle_gare__icontains = recherche
            )
            publications_list = Publication_avis.objects.all().order_by('-date_avis')[:8]
            premiere_ligne = publications_list[:4]
            deuxieme_ligne = publications_list[4:8] 
            context = {
                'details_voyage': Details_voyage.objects.all(),
                'premiere_ligne_pub': premiere_ligne,
                'deuxieme_ligne_pub': deuxieme_ligne,
                'details_voyage_recherches' : details_voyage_recherches,
            }

            return render(request, 'front/index.html', context)
        else:
            publications_list = Publication_avis.objects.all().order_by('-date_avis')[:8]
    
    
            premiere_ligne = publications_list[:4]
            deuxieme_ligne = publications_list[4:8] 

            context = {
                'details_voyage': Details_voyage.objects.all(),
                'premiere_ligne_pub': premiere_ligne,
                'deuxieme_ligne_pub': deuxieme_ligne,
                'details_voyage_recherche' : Details_voyage.objects.all(),
            }

            return render(request, 'front/index.html', context)




class Bienvenu_onatra(View):
    def get(self,request):
        return render(request, 'front/bienvenu_onatra.html')

    

