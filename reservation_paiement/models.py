from django.db import models
from tarification.models import Tarification
from django.contrib.auth.models import User


class Mode_paiement(models.Model):
    libelle_mode = models.CharField(
        max_length = 100
    )


    def __str__(self):
        return self.libelle_mode


class Paiement(models.Model):

    id_user = models.ForeignKey(User,  null = False , on_delete = models.CASCADE,
                                 
    help_text="id du user"

    )

    email_user = models.CharField(
        max_length=200,
        unique=False,
        blank=True,
        null = False,               
        help_text="email du user",
        default = 'boazkalonji962@gmail.com'

    )




    id_tarification = models.ForeignKey(Tarification,  null = False , on_delete = models.CASCADE,

        help_text="id du categorie"                                 
                                     
    )

    montant_paiement = models.DecimalField(
        max_digits = 8,
        decimal_places = 2,
        default = 0.00,
        null = True,
        blank = True
    )
    id_mode_paiement  = models.ForeignKey(Mode_paiement, on_delete = models.CASCADE,
        help_text="le mode de paiement",
        null = True,
        blank = True  
    )       

    date_paiement = models.DateField(
        null = True,
        blank = True 
    )            
    statut = models.BooleanField(
        null = True,
        blank = True 
    )

    qr_code = models.ImageField(
        upload_to='gares_images/',
        blank=True,               
        null=True ,
        default = '' 
    )
    numero_billet = models.CharField(
        max_length=100,
        verbose_name='numero unique du billet',
        help_text="numero unique du billet",
        null = True,
        blank= True,
        default = 'XXXXXXXX'
    )
    nombre_place_reserve = models.IntegerField(
        default = 1
    )
    
    def __str__(self):
        return f'{self.nombre_place_reserve}{self.montant_paiement} - {self.id_user} - {self.date_paiement} - {self.statut} - {self.id_tarification}'




