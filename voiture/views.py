from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Voiture
from tarification.models import Tarification
from train.models import Train
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
class   creation_voiture(View):


    def get(self,request):
        context = {
            'tarifications' :  Tarification.objects.all(),
            'trains' : Train.objects.all(),
        }
        return render(request,'voiture/voiture.html',context)




    def post(self,request):
        if request.method == 'POST':

            id_train = request.POST.get('id_train')
            id_tarification = request.POST.get('id_tarification')
            num_voiture = request.POST.get('num_voiture')
            nombre_place = request.POST.get('nombre_place')


            if id_train =='' or id_tarification == '' or num_voiture == '':
                return render(request,'voiture/voiture.html')
            else:
                
                nouvelle_voituree = Voiture.objects.create(
                    id_train=Train.objects.get(id = id_train), 
                    id_tarification = Tarification.objects.get(id = id_tarification),
                    numero_voiture = num_voiture,
                    nombre_place = nombre_place)

                return redirect('voiture:lire_voiture')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'voiture/voiture.html')

@login_required
def delete_voiture(request,id, slug):
    voiture = Voiture.objects.get(pk = id)
    voiture.delete()
    return redirect('voiture:lire_voiture')

@login_required
def details_voiture(request, id):
    context = {

        'voiture' : Voiture.objects.get(id = id),

    } 
    return render(request, 'voiture/details_voiture.html', context)

@login_required
def lire_voiture(request):
    context = {

        'voitures' : Voiture.objects.all(),
        'total_compt' : Voiture.objects.count(),
        'tarifications' :  Tarification.objects.all(),
        'trains' : Train.objects.all()
    } 
    return render(request, 'voiture/dashbord_voiture.html', context)

@method_decorator(login_required, name='dispatch')
class   modifier_voiture(View):


    def get(self,request,id,slug):
        context  = {

            'voiture' : get_object_or_404(Voiture,id = id),
            'tarifications' :  Tarification.objects.all(),
            'trains' : Train.objects.all()
        }
        return render(request,'voiture/modifier_voiture.html', context)


    def post(self,request,id,slug):

        if request.method == 'POST':

            id_train = request.POST.get('id_train')
            id_tarification = request.POST.get('id_tarification')
            numero_voiture = request.POST.get('numero_voiture')
            nombre_place = request.POST.get('nombre_place')
            
            voiture = Voiture.objects.get(id=id)

            context  = {

            'erreur' : "la voiture n'existe pas , donc impossible de modifier"
            }
            if voiture is not None:
                voiture.id_train = Train.objects.get(id = id_train)
                voiture.id_tarification = Tarification.objects.get(id = id_tarification)
                voiture.numero_voiture = numero_voiture
                voiture.nombre_place = nombre_place
                voiture.save()
                return redirect('voiture:lire_voiture')
            
            return render(request,'voiture/dashbord_voiture.html', context)
        else:
            context  = {

                'erreur' : "le formulaire n'est pas valide"
            }
            return render(request,'voiture/modifier_voiture.html', context)   



