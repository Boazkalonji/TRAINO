from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm
from django_registration.backends.activation.views import RegistrationView
from django.contrib import messages
from django.http import HttpRequest,HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django_registration.backends.activation.views import RegistrationView 
from django.contrib.auth.decorators import login_required
from reservation_paiement.models import Paiement 
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User 
from django.utils.decorators import method_decorator








def send_welcome_email(user):
    """
    Envoie un e-mail de bienvenue à l'utilisateur nouvellement créé,
    incluant son ID de profil.
    """
    
    # 1. Contexte de l'e-mail (Contient uniquement les données nécessaires)
    context = {
        'username': user.username,
        'user_id': user.id, # L'ID de l'utilisateur
        'user_email': user.email,
        'plateforme_name': 'TRAINO', # Nom de la plateforme pour la personnalisation
    }

    # 2. Rendu du contenu HTML (Le chemin doit être dans un dossier 'templates')
    html_content = render_to_string('utilisateur/comptes/operation_comptes/welcome_email.html', context)
    
    # 3. Construction de l'objet Email
    email = EmailMessage(
        # Sujet de l'e-mail
        f"🎉 Bienvenue sur {context['plateforme_name']} ! Votre ID est {user.id}", 
        
        # Contenu
        html_content,
        
        # Expéditeur et Destinataire
        settings.EMAIL_HOST_USER, 
        [user.email], 
    )
    email.content_subtype = "html" # Pour s'assurer que le HTML est rendu correctement
 
    # 4. Envoi
    try:
        email.send()
        print(f"E-mail de bienvenue envoyé à {user.email}")
    except Exception as e:
        # Enregistrez ou affichez l'erreur pour le débogage
        print(f"Erreur lors de l'envoi de l'e-mail de bienvenue à {user.email} : {e}")


def confirmation_success_email(user):
    """
    Envoie un e-mail confirmant à l'utilisateur que son compte a été confirmé
    et qu'il peut se connecter.
    """
    
    # 1. Contexte de l'e-mail
    context = {
        'username': user.username,
        'user_id': user.id,
        'user_email': user.email,
        'plateforme_name': 'TRAINO', 
        
    }


    html_content = render_to_string('utilisateur/comptes/operation_comptes/confirmation_success_email.html', context)
    

    email = EmailMessage(
      
        f"✅ Votre compte {context['plateforme_name']} est confirmé !", 
        
        html_content,
        settings.EMAIL_HOST_USER, 
        [user.email], 
    )
    email.content_subtype = "html"
 
    # 4. Envoi
    try:
        email.send()
        print(f"E-mail de confirmation de succès envoyé à {user.email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail de confirmation : {e}")


@login_required
def profil(request):
    
    utilisateur_connecte = request.user
    
  
    dernier_paiement_avec_qrcode = Paiement.objects.filter(
        id_user=utilisateur_connecte
    ).order_by('-id').first() 
    

    context = {
        'dernier_qrcode_url': None,
        'numero_billet': None, 
    }


    if dernier_paiement_avec_qrcode:
       
        context['numero_billet'] = dernier_paiement_avec_qrcode.numero_billet
        
        if dernier_paiement_avec_qrcode.qr_code:
            context['dernier_qrcode_url'] = dernier_paiement_avec_qrcode.qr_code.url

 
    return render(request, 'utilisateur/comptes/operation_comptes/profil.html', context)


class   creation_comptes(View):

    template_name = 'utilisateur/comptes/operation_comptes/creation_compte.html'

    def get(self, request):
        return render(request, self.template_name)


    def post(self,request):

        erreur = dict()
        donnees = dict()
        champs = {
            'nom': 'le champ (nom)',
            'postnom': 'le champ (postnom)',
            'prenom': 'le champ (prenom)',
            'email': 'le champ (email)',
            'password' : 'le champ (password)',
        }

        for name, description_name in champs.items():
            valeur = request.POST.get(name, '').strip()

            if not valeur:
                erreur[name] = f'{description_name} est obligatoire'
            else:
                donnees[name] = valeur
        if erreur : 
            return render(request, 'utilisateur/comptes/operation_comptes/creation_compte.html', {'erreur':erreur})
        

        exist = User.objects.filter(email = donnees['email'])

        if '@gmail.com' not in donnees['email'] or len(donnees['password']) < 8:
            erreur['email_non_valide'] = f"le format d'email(@gmail.com) ou du password (max 8 ) n'est pas valide"
            return render(request, 'utilisateur/comptes/operation_comptes/creation_compte.html', {'erreur':erreur})


        if exist:
            erreur['email'] = f"l'utilisateur avec ces cette email existe deja"
            return render(request, 'utilisateur/comptes/operation_comptes/creation_compte.html', {'erreur':erreur})
        
        try:
            user = User.objects.create_user(
                username = donnees['nom'], 
                email = donnees['email'],
                password = donnees['password'],
                first_name = donnees['postnom'],
                last_name = donnees['prenom'],
                is_active= False
                
            )
            send_welcome_email(user)
            return render(request, 'utilisateur/comptes/operation_comptes/confirmation_compte.html', {'erreur':erreur})






            

           


            
         
           




        except Exception as e:
            erreur['general'] = f"erreur au moment de la creation de l\'utilisatuer {e}"
            return render(request, 'utilisateur/comptes/operation_comptes/creation_compte.html', {'erreur':erreur})
        finally:
            pass

class confirmation_compte(View):
    template_name = 'utilisateur/comptes/operation_comptes/confirmation_compte.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self,request):


        
        id = request.POST.get('id')
        id = int(id)
        user = User.objects.get(pk = id)

        
        try:

            if user:
                user.is_active= True
                user.save()
                confirmation_success_email(user)
                print(f'{user.id} {user.username} user  trouver')
                return redirect('utilisateur:login_comptes')
            else:

                erreur= {
                    'erreur' : f" votre identifiant n'est pas correcte creer vous un nouveau compte"
                } 
                print(f'{user.id} {user.username} user non trouver 1')
                return render(request, 'utilisateur/comptes/operation_comptes/creation_compte.html', {'erreur':erreur})


        except Exception as e:
            erreur= {
                'erreur' : f" votre identifiant n'est pas correcte creer vous un nouveau compte"
            } 
            print(f'{user.id} {user.username} user non trouver 2')
            return render(request, 'utilisateur/comptes/operation_comptes/creation_compte.html', {'erreur':erreur})
        finally:
            pass

@method_decorator(login_required, name='dispatch')
class   modifier_compte(View):


    def get(self,request,id):
        context  = {

            'user' : get_object_or_404(User,id = id)
        }
        return render(request, 'utilisateur/comptes/operation_comptes/modifier_compte.html', context)


    def post(self,request,id):

        erreur = dict()
        donnees = dict()
        user_update = get_object_or_404(User, id = id)

        champs = {
            'nom': 'le champ (nom)',
            'postnom': 'le champ (postnom)',
            'prenom': 'le champ (prenom)',
            'email': 'le champ (email)',
            'password' : 'le champ (password)',
        }

        for name, description_name in champs.items():
            valeur = request.POST.get(name, '').strip()

            if not valeur:
                erreur[name] = f'{description_name} est obligatoire'
            else:
                donnees[name] = valeur
        if erreur : 
            return render(request, 'utilisateur/comptes/operation_comptes/modifier_compte.html', {'erreur':erreur})
        

        """
        
            on recupere les utilisateeur avec cette email,
            on exclut l'utilisatuer avec l'id qu'on veut modifier
            exists() verifier si il exist un user qui a cette email
            c'est un Boolean 

        """


        req = User.objects.filter(email = donnees['email'])
        req = req.exclude(id=user_update.id)
        exist = req.exists()

        if '@gmail.com' not in donnees['email'] or len(donnees['password']) < 8:
            erreur['email_non_valide'] = f"le format d'email(@gmail.com) ou du password (max 8 ) n'est pas valide"
            return render(request, 'utilisateur/comptes/operation_comptes/modifier_compte.html', {'erreur':erreur})


        if exist:
            erreur['email'] = f"l'utilisateur avec ces cette email existe deja"
            return render(request, 'utilisateur/comptes/operation_comptes/modifier_compte.html', {'erreur':erreur})
        
        try:

            user_update.username = donnees.get('nom', user_update.username)
            user_update.email = donnees.get('email', user_update.email)
            user_update.first_name = donnees.get('postnom', user_update.first_name)
            user_update.last_name = donnees.get('prenom', user_update.last_name)
            user_update.is_active= True
            user_update.save()

            if 'password' in donnees:
                user_update.set_password(donnees['password'])
                user_update.save()
            
            

            return redirect("utilisateur:login_comptes")

        except Exception as e:
            erreur['general'] = f"erreur au moment de la creation de l\'utilisatuer {e}"
            return render(request, 'utilisateur/comptes/operation_comptes/modifier_compte.html', {'erreur':erreur})
        finally:
            pass

#@method_decorator(login_required, name='dispatch')
class login_comptes(View):



    def get(self, request):
        return render(request, 'utilisateur/comptes/operation_comptes/login.html')
    

    
    



    def post(self,request):



        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()


        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('front:index')
            
        else:
            context = {
                'erreur' : "les comptes avec ces informations n'a pas été trouver creez vous un compte"
            }
            return render(request, 'utilisateur/comptes/operation_comptes/login.html', context)
        
@method_decorator(login_required, name='dispatch')
class logout_compte(View):

    def get(relf, request):
        logout(request)
        return redirect('utilisateur:login_comptes')
    
@method_decorator(login_required, name='dispatch')
class supprimer_compte(View):

    def get(self,request,id):


        delete_user = get_object_or_404(User,id = id)
        delete_user.delete()
        return redirect('utilisateur:login_comptes')










