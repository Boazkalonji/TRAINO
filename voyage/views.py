from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Voyage
from train.models import Train
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
class   creation_voyage(View):


    def get(self,request):
        context = {
                    'trains' : Train.objects.all()
                }
        return render(request,'voyage/voyage.html',context)




    def post(self,request):
        if request.method == 'POST':

            id_train = request.POST.get('id_train')
            date_depart = request.POST.get('date_depart')
            heure_depart = request.POST.get('heure_depart')



            if id_train =='' :
                return render(request,'voyage/voyage.html')
            else:
                
                nouvelle_voyage = Voyage.objects.create(
                    id_train=Train.objects.get(id = id_train),
                    date_depart = date_depart,
                    heure_depart = heure_depart)

                return redirect('voyage:lire_voyage')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'voyage/voyage.html')

@login_required
def delete_voyage(request,id, slug):
    voyage = Voyage.objects.get(pk = id)
    voyage.delete()
    return redirect('voyage:lire_voyage')

@login_required
def details_voyage(request, id):
    context = {

        'voyage' : Voyage.objects.get(id = id),

    } 
    return render(request, 'voyage/details_voyage.html', context)

@login_required
def lire_voyage(request):
    context = {

        'voyages' : Voyage.objects.all(),
        'total_compt' : Voyage.objects.count(),
        'trains' : Train.objects.all()
    } 
    return render(request, 'voyage/dashbord_voyage.html', context)

@method_decorator(login_required, name='dispatch')
class   modifier_voyage(View):


    def get(self,request,id,slug):
        context  = {

            'voyage' : get_object_or_404(Voyage,id = id),
            'trains' : Train.objects.all()
        }
        return render(request,'voyage/modifier_voyage.html', context)


    def post(self,request,id,slug):

        if request.method == 'POST':

            id_train = request.POST.get('id_train')
            date_depart = request.POST.get('date_depart')
            heure_depart = request.POST.get('heure_depart')
     
            
            voyage = Voyage.objects.get(id=id)

            context  = {

            'erreur' : "la voyage n'existe pas , donc impossible de modifier"
            }
            if voyage is not None:
                voyage.id_train = Train.objects.get(id = id_train)
                voyage.date_depart = date_depart
                voyage.heure_depart = heure_depart
                voyage.save()
                return redirect('voyage:lire_voyage')
            
            return render(request,'voyage/dashbord_voyage.html', context)
        else:
            context  = {

                'erreur' : "le formulaire n'est pas valide"
            }
            return render(request,'voyage/modifier_voyage.html', context)   




