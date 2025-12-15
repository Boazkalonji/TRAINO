from django.db import models
from tarification.models import Tarification

class Publication_avis(models.Model):
    reference_avis = models.TextField(

        verbose_name='reference_avis ',
        help_text="reference_avis",
        null = False,
        blank= False,
    )


    titre_avis = models.TextField(

        verbose_name='titre_avis',
        help_text="titre_avis",
        null = False,
        blank= False,
    )

    message_avis = models.TextField(

        verbose_name='message_avis',
        help_text="message_avis",
        null = False,
        blank= False,
    )

    date_avis = models.DateField()

    consigne_avis = models.TextField(

        verbose_name='consigne_avis',
        help_text="consigne_avis",
        null = False,
        blank= False,
    )
    slug = models.SlugField(
        default="jkjkhjdhjdhjzhjezjkoiuehb5kskhjbvbzhj5685dhhzehjjkehjzhjehhjcncjkzzjkzoiioeuiuirhcbzbnklqkdhshdbbb",
        max_length= 100
    )

    def __str__(self):
        return f"{self.reference_avis} {self.consigne_avis} {self.date_avis} {self.titre_avis} {self.message_avis}"









class Pubilaction_tarification(models.Model):

    id_tarification = models.ForeignKey(Tarification,  null = False , on_delete = models.CASCADE,

        help_text="id dela Tarification"                                 
                                     
    )

    id_pubilaction_avis = models.ForeignKey(Publication_avis,  null = False , on_delete = models.CASCADE,

        help_text="id dela Publication_avis"                                 
                                     
    )

    slug = models.SlugField(
        default="jkjkhjdhjdhjzhjezjkoiuehb5kskhjbvbzhj5685dhhzehjjkehjzhjehhjcncjkzzjkzoiioeuiuirhcbzbnklqkdhshdbbb",
        max_length= 100
    )


    def __str__(self):
        return f"{self.id_tarification} {self.id_pubilaction_avis}"




