from django.db import models


class Gare(models.Model):
    libelle_gare = models.CharField(
        max_length=20,
        verbose_name='libelle du gare',
        help_text="rlibelle du gare",
        null = False,
        blank= False,
    )


    ville_gare = models.CharField(
        max_length=20,
        verbose_name='ville du gare',
        help_text="ville du gare",
        null = False,
        blank= False,
    )





    slug = models.SlugField(
        default="02Kkjsdhjfhf655qqzasjqsdbbbz555sc6JHMSLR",
        max_length= 100
    )

    def __str__(self):
        return self.libelle_gare

