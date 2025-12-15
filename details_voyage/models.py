from django.db import models

from gare.models import Gare
from voyage.models import Voyage


class Details_voyage(models.Model):

    id_voyage = models.ForeignKey(Voyage,  null = False , on_delete = models.CASCADE,
                                 
    help_text="id du voyage"

    )
    id_gare_depart = models.ForeignKey(Gare,  null = False , on_delete = models.CASCADE,

        help_text="id dela Gare de part",
        related_name='voyages_au_depart'
                                      
                                     
    )
    id_gare_arrive = models.ForeignKey(Gare,  null = False , on_delete = models.CASCADE,

        help_text="id dela Gare d'arrivee",
        related_name='voyages_a_larrivee'                                
                                     
    )
    distance = models.IntegerField(
        verbose_name='distance entre la gare de depart et d\'arrivée',
        help_text="distance entre la gare de depart et d\'arrivée",
        null = True,
        blank= True,
    )


    image = models.ImageField(
        upload_to='gares_images/', 
        blank=False,               
        null=False                 
    )

    slug = models.SlugField(
        default="distanceGareLPPZNN025SN02Kkjsdhjfhf655qqzasjqsdbbbz555sc6JHMSLR",
        max_length= 100
    )

    def __str__(self):
        return f"{self.image}  {self.id_voyage} - {self.id_gare_depart} - {self.id_gare_arrive} - {self.distance}"




