from django.db import models
from train.models import Train

class Voyage(models.Model):

    id_train = models.ForeignKey(Train,  null = False , on_delete = models.CASCADE,
        verbose_name='numero d\'un train exemple A-0000 qui effectuer un voyage',
        help_text='numero d\'un train exemple A-0000 qui effectuer un voyage',
        blank= False
    )
    heure_depart = models.TimeField()
    date_depart = models.DateField()

    slug = models.SlugField(
        default="02Kkjsdhjfhf655qqzasjqsdbbbz555sc6JHMSLR",
        max_length= 100
    )

    def __str__(self):
        return f"le numero train pour ce voyage{self.id_train} la date: {self.date_depart} - {self.heure_depart}"

