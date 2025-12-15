import random
import string
import re



def generer_num_billet(longueur=10):


    lettres = string.ascii_letters
    chiffres = string.digits
    symboles = '!@#$%^&*' 
    tous_les_caracteres = lettres + chiffres + symboles
    
    chaine_resultat = []
    chaine_resultat.append(random.choice(lettres)) 

    chaine_resultat.append(random.choice(chiffres))

    chaine_resultat.append(random.choice(symboles))
    
    restant_a_generer = longueur - len(chaine_resultat)
    
    caracteres_restants = random.choices(tous_les_caracteres, k=restant_a_generer)
    chaine_resultat.extend(caracteres_restants)
    
    
    random.shuffle(chaine_resultat)
    
    
    return "".join(chaine_resultat)



print("Chaîne générée :", generer_num_billet(10)) 
print("Chaîne de 15 caractères :", generer_num_billet(15))

















def extraire_initiales_gare(libelle):

    libelle = libelle.replace('-', ' ').replace("'", ' ')
    

    mots = libelle.split()
    
    initiales = []
    

    mots_a_ignorer = ['de', 'du', 'la', 'le', 'les', 'des', 'et']
    
    for mot in mots:
        
        mot_nettoye = mot.lower()
        if mot_nettoye and mot_nettoye not in mots_a_ignorer:
            initiales.append(mot[0].upper())
            
    
    if not initiales and libelle:
        return libelle[:2].upper()

    return "".join(initiales)