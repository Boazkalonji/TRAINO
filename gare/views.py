from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .models import Gare
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required





@method_decorator(login_required, name='dispatch')
class   creation_gare(View):


    def get(self,request):
        return render(request,'gare/gare.html')




    def post(self,request):
        if request.method == 'POST':

            libelle_gare = request.POST.get('libelle_gare')
            ville_gare = request.POST.get('ville_gare')



            if libelle_gare =='' or ville_gare == '':
                return render(request,'gare/gare.html')
            else:
                
                nouvelle_gare = Gare.objects.create(
                    libelle_gare = libelle_gare,
                    ville_gare = ville_gare
                )

                return redirect('gare:lire_gare')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'gare/gare.html')

@login_required
def delete_gare(request,id, slug):
    gare = Gare.objects.get(pk = id)
    gare.delete()
    return redirect('gare:lire_gare')

@login_required
def details_gare(request, id):
    context = {

        'gare' : Gare.objects.get(id = id),

    } 
    return render(request, 'gare/details_gare.html', context)


@login_required
def lire_gare(request):
    context = {

        'gares' : Gare.objects.all(),
        'total_compt' : Gare.objects.count(),
    } 
    return render(request, 'gare/dashbord_gare.html', context)

@method_decorator(login_required, name='dispatch')
class   modifier_gare(View):


    def get(self,request,id,slug):
        context  = {

            'gare' : get_object_or_404(Gare,id = id),
        }
        return render(request,'gare/modifier_gare.html', context)


    def post(self,request,id,slug):

        if request.method == 'POST':

            libelle_gare = request.POST.get('libelle_gare')
            ville_gare = request.POST.get('ville_gare')

            
            gare = Gare.objects.get(id=id)

            context  = {

            'erreur' : "la gare n'existe pas , donc impossible de modifier"
            }
            if gare is not None:
                gare.libelle_gare = libelle_gare
                gare.ville_gare =ville_gare

                gare.save()
                return redirect('gare:lire_gare')
            
            return render(request,'gare/dashbord_gare.html', context)
        else:
            context  = {

                'erreur' : "le formulaire n'est pas valide"
            }
            return render(request,'gare/modifier_gare.html', context)   



