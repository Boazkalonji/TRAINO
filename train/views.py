from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from .models import Train
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class   creation_train(View):


    def get(self,request):
        return render(request,'train/train.html')




    def post(self,request):
        if request.method == 'POST':

            numero_train = request.POST.get('numero_train')
            taille_ram = request.POST.get('taille_ram')
            couleur = request.POST.get('couleur')



            if numero_train =='' or taille_ram == '' or couleur =='':
                return render(request,'train/train.html')
            else:
                
                nouvelle_gare = Train.objects.create(
                    numero_train = numero_train,
                    taille_ram = taille_ram,
                    couleur = couleur

                )

                return redirect('train:lire_train')
        else:
            context = {
                'erreur' : 'le formulaire ne pas soumis veuillez revoir les informations saisies'
            }
            return render(request,'train/train.html')

@login_required
def delete_train(request,id, slug):
    train = Train.objects.get(pk = id)
    train.delete()
    return redirect('train:lire_train')

@login_required
def details_train(request, id):
    context = {

        'train' : Train.objects.get(id = id),

    } 
    return render(request, 'train/details_train.html', context)

@login_required
def lire_train(request):
    context = {

        'trains' : Train.objects.all(),
        'total_compt' : Train.objects.count(),
    } 
    return render(request, 'train/dashbord_train.html', context)

@method_decorator(login_required, name='dispatch')
class   modifier_train(View):


    def get(self,request,id,slug):
        context  = {

            'train' : get_object_or_404(Train,id = id),
        }
        return render(request,'train/modifier_train.html', context)


    def post(self,request,id,slug):

        if request.method == 'POST':

            numero_train = request.POST.get('numero_train')
            taille_ram = request.POST.get('taille_ram')
            couleur = request.POST.get('couleur')
            
            train = Train.objects.get(id=id)

            context  = {

            'erreur' : "la train n'existe pas , donc impossible de modifier"
            }
            if train is not None:
                train.numero_train = numero_train
                train.taille_ram =taille_ram
                train.couleur = couleur

                train.save()
                return redirect('train:lire_train')
            
            return render(request,'train/dashbord_train.html', context)
        else:
            context  = {

                'erreur' : "le formulaire n'est pas valide"
            }
            return render(request,'train/modifier_train.html', context)   



