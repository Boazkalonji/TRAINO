from django import forms
from gare.models import Gare 


class TrajetForm(forms.Form):
    
    
    depart = forms.ModelChoiceField(
        queryset=Gare.objects.all().order_by('libelle_gare'),
        label="Gare de Départ",
        
        
        
        
        empty_label="--- Choisir la gare de départ ---"
    )
    
    arrivee = forms.ModelChoiceField(
        queryset=Gare.objects.all().order_by('libelle_gare'),
        label="Gare d'Arrivée",
    
        
        empty_label="--- Choisir la gare d'arrivée ---"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        depart = cleaned_data.get("depart")
        arrivee = cleaned_data.get("arrivee")

        if depart == arrivee:
            raise forms.ValidationError(
                "La gare de départ ne peut pas être la même que la gare d'arrivée."
                
            )
        return cleaned_data