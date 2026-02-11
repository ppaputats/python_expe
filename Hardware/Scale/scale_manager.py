# ---------------------------------------------------------
# Importation
# ---------------------------------------------------------

from Hardware.Scale.scale import Connection_scale, Send_scale, Close_scale
from Software.Config.config_manager import ConfigManager

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

config = ConfigManager()

# ---------------------------------------------------------
# Scale Manager
# ---------------------------------------------------------

def read_weight(mode):
    """
    mode : "palette" ou "colis"
    Retourne le poids mesuré ou None si erreur
    """
    print("read_weight entree")
    # Sélection de la balance selon le mode
    if mode == "palette":
        id_scale = config.get("scale_palette")
    elif mode == "colis":
        id_scale = config.get("scale_colis")
    else:
        print("Erreur : mode inconnu", mode)
        return None

    # Connexion
    if not Connection_scale(id_scale):
        print(f"Erreur : impossible de se connecter à la balance {id_scale}")
        return None

    # Lecture du poids
    """try:
        poids = float(poids.replace("kg", "").strip())
    except:
        poids = None"""

    try:
        poids = Send_scale(id_scale)
    except Exception as e:
        print("Erreur lors de la lecture du poids :", e)
        Close_scale(id_scale)
        return None

    Close_scale(id_scale)
    print("read_weight entree")
    return poids
