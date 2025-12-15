from django.db import models


class Train(models.Model):

    numero_train = models.CharField(
        max_length=10,
        verbose_name='numero voiture exemple A-0000',
        help_text="un sert de clé secondaire à la table voiture",
        null = False,
        blank= False,
    )
    taille_ram = models.IntegerField(

        verbose_name='taille_ram',
        help_text="taille_ram",
        null = False,
        blank= False,

    )

    couleur = models.CharField(
        max_length=30,
        verbose_name='couleur',
        help_text="couleur",
        null = False,
        blank= False,
        default = 'pas de couleur',

    )

    slug = models.SlugField(
        default="02Kkjsdhjfhf655qqzasjqsdbbbz555sc6JHMSLR",
        max_length= 100
    )

    def __str__(self):
        return f"{self.numero_train} - {self.couleur} - {self.taille_ram}"
