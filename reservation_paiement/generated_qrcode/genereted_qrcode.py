import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from typing import TextIO, Any


def genereted_qrcode(valeur: str) -> ContentFile:
    """
    Génère un QR code à partir de la valeur fournie, l'encode en PNG
    et le retourne sous forme de ContentFile utilisable par Django.

    Args:
        valeur (str): La donnée à encoder dans le QR code (ex: un identifiant de réservation).

    Returns:
        ContentFile: Le fichier PNG du QR code prêt à être sauvegardé dans un modèle.
    """
    
    # 1. Création de l'objet QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(valeur)
    qr.make(fit=True)
    

    img: Any = qr.make_image(fill_color="black", back_color="white")


    buffer: TextIO = BytesIO()


    img.save(buffer, "PNG")


    buffer.seek(0)
    """
    Une fois l'image enregistrée dans le buffer, cette ligne remet le curseur à zéro (au début)
    afin que 'buffer.read()' puisse lire l'intégralité du contenu depuis le début.
    """

    nom_file: str = f'qr_code_{valeur.replace("/", "_")}.png'


    return ContentFile(buffer.read(), name=nom_file)

