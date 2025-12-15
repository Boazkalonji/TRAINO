from django.db import models
from voyage.models import Voyage
from details_voyage.models import Details_voyage





class Tarification(models.Model):


    id_details_voyage = models.ForeignKey(Details_voyage,  null = False , on_delete = models.CASCADE,
                                 
    help_text="id du voyage"

    )
    pu  = models.IntegerField(
        default=0,
        verbose_name="tarification elementaire pour une categorie",
        help_text="prix unitaire categorie = tarification"
    )

    designation_tarififcation = models.CharField(
        max_length=10,
        verbose_name='designation',
        help_text="designation Tarififcation",
        null = False,
        blank= False,
    )
    slug = models.SlugField(
        default="02KJHMSLRTarififcationooopp8225hgqgqgnndnenxxxjk//5",
        max_length= 100
    )
    def __str__(self):
        return f"{self.pu} {self.designation_tarififcation} {self.id_details_voyage}"












""""















class siege(models.Model):

    id_voiture = models.ForeignKey('voiture',  null = False , on_delete = models.CASCADE)
    numero_siege  = models.CharField(
        max_length=10,
        verbose_name='numero siege exemple A-0000',
        help_text="un sert de clé secondaire à la table siege",
        null = True,
        blank= True,
    )

    ranger  = models.CharField(
        max_length=10,
        verbose_name='ranger du siege',
        help_text="ranger A , siege A-1",
        null = True,
        blank= True,
    )

    def __str__(self):
        return self.numero_siege + " " + self.id_voiture + " " + self.ranger





"""