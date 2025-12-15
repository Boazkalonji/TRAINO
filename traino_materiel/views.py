from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Categorie



""" debut Gestion categorie"""

class   creation_categorie(View):


    def get(self,request):
        return render(request,'traino_materiel/categorie.html')




    def post(self,request):
        if request.method == 'POST':

            tarification_float = float(request.POST.get('tarif').replace(',', '.'))
            tarif = int(tarification_float)
            designation_categorie = request.POST.get('designation_categorie')


            if tarif =='' or designation_categorie == '':
                context = {
                    'erreur' : 'les champs obligatoire'
                }
                return render(request,'traino_materiel/categorie.html',context )
            else:
                
                nouvelle_categorie = Categorie.objects.create(tarif=tarif, designation_categorie=designation_categorie)

                return redirect('traino_materiel:lire_categorie')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'traino_materiel/categorie.html')



def delete_categorie(request,id, slug):
    categorie = Categorie.objects.get(pk = id)
    categorie.delete()
    return redirect('traino_materiel:lire_categorie')


def details_categorie(request, id):
    context = {

        'categorie' : Categorie.objects.get(id = id),

    } 
    return render(request, 'traino_materiel/details_categorie.html', context)



def lire_categorie(request):
    context = {

        'categories' : Categorie.objects.all(),
        'total_compt' : Categorie.objects.count()
    } 
    return render(request, 'traino_materiel/dashbord_categorie.html', context)





class   modifier_categorie(View):


    def get(self,request,id,slug):
        context  = {

            'categorie' : get_object_or_404(Categorie,id = id)
        }
        return render(request,'traino_materiel/modifier_categorie.html', context)


    def post(self,request,id,slug):

        if request.method == 'POST':

            tarif = request.POST['tarif']
            designation_categorie = request.POST['designation_categorie']
            
            categorie = Categorie.objects.get(id=id)

            context  = {

            'erreur' : "le categorie n'existe pas , donc impossible de modifier"
            }
            if categorie is not None:
                categorie.tarif = tarif
                categorie.designation_categorie = designation_categorie
                categorie.save()
                return redirect('traino_materiel:dashbord_categorie')
            
            return render(request,'traino_materiel/dashbord_categorie.html', context)
        else:
            context  = {

                'erreur' : "le formulaire n'est pas valide"
            }
            return render(request,'traino_materiel/modifier_categorie.html', context)   



"""Fin gestion categorie"""


























