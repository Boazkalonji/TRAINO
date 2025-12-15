from django.db import models






class Categorie(models.Model):
    tarif  = models.IntegerField(
        default=0,
        verbose_name="tarification total pour une categorie",
        help_text="prix unitaire categorie = tarification"
    )

    designation_categorie = models.CharField(
        max_length=10,
        verbose_name='designation',
        help_text="designation categorie",
        null = False,
        blank= False,
    )
    slug = models.SlugField(
        default="02KJHMSLR",
        max_length= 100
    )
    def __str__(self):
        return f"{self.tarif} {self.designation_categorie}"












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