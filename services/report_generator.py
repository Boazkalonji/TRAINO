import subprocess
import os
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from tarification.models import Tarification # Assurez-vous d'importer Tarification si la logique est déplacée

# --- CHEMINS ET CONFIGURATION ---

# IMPORTANT : REMPLACER PAR VOTRE CHEMIN EXACT DE JASPERSTARTER.EXE
#JASPERSTARTER_EXE_PATH = r"C:\Program Files\jasperstarter\bin\jasperstarter.exe" 
JASPERSTARTER_JAR_PATH = r"C:\Program Files\jasperstarter\lib\jasperstarter.jar"

# Chemin vers le driver JDBC que vous avez placé dans /drivers/
DRIVER_FILENAME = 'postgresql-42.3.1.jar' 
DRIVER_PATH = os.path.join(settings.BASE_DIR, 'drivers', DRIVER_FILENAME) 

# NOUVEAU: Chemin vers le DOSSIER contenant les drivers
JDBC_DIR = os.path.join(settings.BASE_DIR, 'drivers')



#IMAGE_RESOURCE_DIR = r"C:\Users\hp\JaspersoftWorkspace\MyReports"



IMAGE_RESOURCE_DIR = os.path.join(settings.BASE_DIR, 'reports', 'report_images')
os.makedirs(IMAGE_RESOURCE_DIR, exist_ok=True)


# Chemin vers votre fichier .jasper (rapport_jour_cash.jasper)
JRXML_FILES_DIR = os.path.join(settings.BASE_DIR, 'reports', 'jasper_files')

# Dossier où le PDF sera sauvegardé temporairement
OUTPUT_DIR = os.path.join(settings.BASE_DIR, 'media', 'reports') 


# NOUVEAU: Chemin vers votre Java 8 JRE/JDK
JAVA8_EXE_PATH = r"C:\Program Files\Eclipse Adoptium\jdk-8.0.472.8-hotspot\bin\java.exe" 
# ...


# ---------------------------------------------

def generer_pdf_local(jasper_filename, output_filename, db_config, parameters=None):
    """
    Appelle jasperstarter en utilisant le chemin d'accès direct.
    """
    
    # 1. Préparation des chemins
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    jasper_path = os.path.join(JRXML_FILES_DIR, jasper_filename)
    output_path_base = os.path.join(OUTPUT_DIR, output_filename.replace('.pdf', ''))

    # 2. Arguments de connexion à la base de données
    db_args = [
        '-t', 'postgres', 
        '-H', db_config['HOST'],
        '-u', db_config['USER'],
        '-p', db_config['PASS'],
        '-n', db_config['NAME'], 
        '--jdbc-dir', JDBC_DIR 
    ]
    
    # Ajouter le port si spécifié (si vous avez modifié le port par défaut 5432)
    if 'PORT' in db_config and db_config['PORT']:
        # L'option -P dans jasperstarter est pour les paramètres, mais -p est le mot de passe
        # Pour le port non standard, on doit souvent utiliser l'option --db-port
        db_args.extend(['--db-port', db_config['PORT']])

    # 3. Construction de la commande (Lancement direct de l'EXE)


    param_args = []
    if parameters:
        # L'option de JasperStarter pour les paramètres est -P nom=valeur
        for key, value in parameters.items():
            param_args.extend(['-P', f'{key}={value}'])






    
    command = [
        JAVA8_EXE_PATH,
        '-Djava.awt.headless=true',
        '-jar', 
        JASPERSTARTER_JAR_PATH, # <-- CORRECTION 1 : AJOUT DU CHEMIN DU JAR
        
        'pr', # Process Report
        jasper_path,
        *db_args,

        *param_args,
        '-r', IMAGE_RESOURCE_DIR,
        '-o', output_path_base,
        '-f', 'pdf' 
    ]








    print("Commande JasperStarter complète :", " ".join(command))
    try:
        # 5. Exécution de la commande
        result = subprocess.run(command, check=True, capture_output=True, text=True) 
        
        final_pdf_path = output_path_base + '.pdf'
        
        if os.path.exists(final_pdf_path):
            return final_pdf_path
        else:
            return None

    except subprocess.CalledProcessError as e:
        # Affiche l'erreur si jasperstarter échoue (problème de DB, de rapport, ou de lancement)
        print(f"Erreur d'exécution de JasperStarter : Code {e.returncode}")
        print(f"Stdout (sortie standard) : {e.stdout}")
        print(f"Stderr (sortie d'erreur) : {e.stderr}")
        print(f"Stderr de JasperStarter (ERREUR) : {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Erreur Fatale: Exécutable non trouvé à {JASPERSTARTER_JAR_PATH}. Vérifiez le chemin.")
        return None




    



























# Fichier : Où se trouve render_to_pdf/link_callback

def link_callback(uri, rel):
    # 1. Nettoyer l'URI (ex: /static/css/publication_avis/publication_avis.css -> css/publication_avis/publication_avis.css)
    path_relatif = uri.replace(settings.STATIC_URL, "")
    
    # 2. ESSAYER le chemin direct dans STATIC_ROOT (ce qui a échoué)
    chemin_direct = os.path.join(settings.STATIC_ROOT, path_relatif)
    
    # 3. ESSAYER le chemin avec le nom de l'application (le chemin collecté par Django)
    
    # Exemple : extrait 'publication_avis' de l'URI (peut être plus complexe si URI ne contient pas app_name)
    # L'image 'img/onatra.png' vient du dossier 'publication_avis/static/img/onatra.png'
    # On va vérifier si le chemin existe dans la base des statiques collectées.
    
    # Chemin sur le disque de Render pour les statiques collectées
    # (Nous supposons que 'css' ou 'img' est le premier dossier après l'application)
    
    # Tentons une approche plus simple : si le fichier n'est pas trouvé dans le chemin direct,
    # nous le cherchons dans un sous-dossier portant le nom de l'application.
    
    # Déterminons le nom de l'application (ici 'publication_avis' pour le CSS et 'onatra.png')
    app_name = 'publication_avis' # à adapter si l'image vient d'une autre app comme 'base' ou 'assets'
    
    # Chemin avec le nom de l'application (le chemin le plus probable en prod)
    chemin_app = os.path.join(settings.STATIC_ROOT, app_name, path_relatif)

    # DÉCISION
    if os.path.isfile(chemin_direct):
        return chemin_direct
        
    elif os.path.isfile(chemin_app):
        return chemin_app
        
    else:
        # Si vous arrivez ici, rien n'a été trouvé.
        print(f"FICHIER STATIQUE MANQUANT DANS TOUS LES CHEMINS: {chemin_direct} OU {chemin_app}")
        # Si c'est un fichier critique (CSS/Image), on retourne None pour signaler l'erreur
        return None


















def render_to_pdf(template_src, context_dict={}):
    """
    Convertit un template Django en PDF en utilisant xhtml2pdf.
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    
    result = BytesIO()
    
    pisa_status = pisa.CreatePDF(
        html, 
        dest=result,
        # UTILISEZ LA FONCTION link_callback DÉFINIE CI-DESSUS
        link_callback=link_callback 
    )
    
    if pisa_status.err:
        return None 
    return result.getvalue()











