# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

id_camera = [0, 1, 2] #  0 => colis, 1,2 => palette

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------


def Connection_camera(id_camera):
       
    """
    Fonction : Ouvre la connexion avec la camera choisie
    Entrée : id_camera
    Sortie : Booléen de connexion
    """
    
    print("Hello Connection_camera")
    return True

def Photo_camera(id_camera, path, parent=None):
       
    """
    Fonction : Prends une photo avec la caméra selectionnée
    Entrée : id_camera
    Sortie : Chemin de stockage de la photo
    """
    
    file, _ = QFileDialog.getOpenFileName(parent, "Choisir photo")
    print("Hello Photo_camera")
    return file 

def Close_camera(id_camera):
           
    """
    Fonction : Ferme le connexion avec la caméra
    Entrée : id_camera
    Sortie : Booléen de fermeture
    """
    
    print("Hello Close_camera")
    return
