from django.db import models

from tarification.models import Tarification
from train.models import Train


class Voiture(models.Model):

    id_train = models.ForeignKey(Train,  null = False , on_delete = models.CASCADE,
                                 
    help_text="id du train"

    )
    id_tarification = models.ForeignKey(Tarification,  null = False , on_delete = models.CASCADE,

        help_text="id du categorie"                                 
                                     
    )

    numero_voiture = models.CharField(
        max_length=10,
        verbose_name='numero voiture exemple A-0000',
        help_text="un sert de clé secondaire à la table voiture",
        null = True,
        blank= True,
    )
    nombre_place = models.IntegerField(
        default=0
    )

    slug = models.SlugField(
        default="02Kkjsdhjfhf655qqzasjqsdbbbz555sc6JHMSLR",
        max_length= 100
    )

    def __str__(self):
        return f"{self.numero_voiture} - {self.nombre_place}"




