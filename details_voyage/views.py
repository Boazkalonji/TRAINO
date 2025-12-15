from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Details_voyage
from voyage.models import Voyage
from gare.models import Gare
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
class   creation_details_voyage(View):


    def get(self,request):
        context = {'voyages' :  Voyage.objects.all(),
                    'gares' : Gare.objects.all()
                    }
        return render(request,'details_voyage/details_voyage.html',context)




    def post(self,request):
        if request.method == 'POST':

            id_voyage = request.POST.get('id_voyage')
            id_gare_depart = request.POST.get('id_gare_depart')
            id_gare_arrive = request.POST.get('id_gare_arrive')
            image = request.FILES.get('image')
            distance = request.POST.get('distance')


            if id_voyage =='' or id_gare_depart == '' or id_gare_arrive == '' or distance == '':
                return render(request,'details_voyage/details_voyage.html')
            else:
                
                if id_gare_depart == id_gare_arrive:

                    context = {
                        'erreur' : 'le point de depart et d\'arriver sont pareils'
                    }
                    return render(request,'details_voyage/details_voyage.html', context)
                else:
                    nouvelle_details_voyage = Details_voyage.objects.create(
                    id_voyage=Voyage.objects.get(id = id_voyage), 
                    id_gare_depart=Gare.objects.get(id = id_gare_depart),
                    id_gare_arrive = Gare.objects.get(id = id_gare_arrive),
                    image = image,
                    distance = distance)
                return redirect('details_voyage:lire_details_voyage')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'details_voyage/details_voyage.html', context)

@login_required
def delete_details_voyage(request,id, slug):
    details_voyage = Details_voyage.objects.get(pk = id)
    details_voyage.delete()
    return redirect('details_voyage:lire_details_voyage')

@login_required
def details_details_voyage(request, id):
    context = {

        'details_voyage' : Details_voyage.objects.get(id = id),

    } 
    return render(request, 'details_voyage/details_details_voyage.html', context)

@login_required
def lire_details_voyage(request):
    context = {

        'voyages' : Voyage.objects.all(),
        'gares' : Gare.objects.all(),
        'total_compt' : Details_voyage.objects.count(),
        'details_voyages' :  Details_voyage.objects.all(),

    } 
    return render(request, 'details_voyage/dashbord_details_voyage.html', context)

@method_decorator(login_required, name='dispatch')
class   modifier_details_voyage(View):


    def get(self,request,id,slug):
        context  = {

            'voyages' : Gare.objects.all(),
            'gares' :  Gare.objects.all(),
            'details_voyage' : get_object_or_404(Details_voyage,id = id)
        }
        return render(request,'details_voyage/modifier_details_voyage.html', context)


    def post(self,request,id,slug):

        if request.method == 'POST':

            id_voyage = request.POST.get('id_voyage')
            id_gare_depart = request.POST.get('id_gare_depart')
            id_gare_arrive = request.POST.get('id_gare_arrive')
            image = request.FILES.get('image')
            distance = request.POST.get('distance')

            if id_gare_depart == id_gare_arrive:
                context = {
                    'erreur' : 'le point de depart et d\'arriver sont pareils'
                }
                return render(request,'details_voyage/modifier_details_voyage.html', context)
            
            details_voyage = Details_voyage.objects.get(id=id)

            context  = {

                'erreur' : "la trajet n'existe pas , donc impossible de modifier"
            }
            if details_voyage is not None:
                details_voyage.id_voyage = Voyage.objects.get(id = id_voyage)
                details_voyage.id_gare_depart = Gare.objects.get(id = id_gare_depart)
                details_voyage.id_gare_arrive = Gare.objects.get(id = id_gare_arrive)
                details_voyage.distance = distance
                details_voyage.image = image
                details_voyage.save()
                return redirect('details_voyage:lire_details_voyage')
            
            return render(request,'details_voyage/dashbord_details_voyage.html', context)
        else:
            context  = {

                'erreur' : "le formulaire n'est pas valide"
            }
            return render(request,'details_voyage/modifier_details_voyage.html', context)   



