# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from Software.Config.config_manager import ConfigManager

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

config = ConfigManager()

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

def Connection_scale(id_scale):

    """
    Fonction : Ferme la liason avec la balance
    Entrée : id de la balance
    Sortie : True si connection ok
    """
    camera=config.get(id_scale)     
    return True

import random

def Send_scale(id_scale):
    #com = config.get(id_scale)
    """
    Fonction : Lance une mesure de poids et retourne la mesure
    Entrée : id de la balance
    Sortie : Poids de la mesure
    """
    print("Poids")
    camera=config.get(id_scale)     
    return random.random() * 100


def Close_scale(id_scale):

    """
    Fonction : Ferme la liason avec la balance
    Entrée : id de la balance
    Sortie : True si liason bien fermée
    """
    camera=config.get(id_scale)          
    return True


"""
def Connection_scale(id_scale): 
    """ 
    #Ouvre le port COM correspondant à la balance
    #id_scale = clé config (ex : 'balance_palette') 
""" 
    global serial_conn port = config.get(id_scale)
    if not port: 
        print("Port non défini dans config :", id_scale) 
        return False 
    try: 
        serial_conn = serial.Serial( port=port, baudrate=9600, timeout=1 ) 
        print("Connexion balance OK :", port) 
        return True 
    except Exception as e: 
        print("Erreur ouverture port :", e) 
        serial_conn = None 
        return False 
    
def Send_scale(id_scale): 
    """ 
    #Envoie la commande ASCII pour demander le poids et lit la réponse. 
""" 
    global serial_conn 
    if serial_conn is None or not serial_conn.is_open: 
        print("Port non ouvert") 
        return None 
    try: 
        # Exemple : commande ASCII "P" + CRLF 
        serial_conn.write(b"P\r\n") 
        # Lecture de la réponse 
        raw = serial_conn.readline().decode("ascii").strip() 
        print("Réponse brute balance :", raw) 
        return raw 
    except Exception as e: 
        print("Erreur lecture balance :", e) 
        return None 
    
def Close_scale(id_scale): 
    """ 
    #Ferme le port COM 
"""
    global serial_conn 
    if serial_conn and serial_conn.is_open: 
        serial_conn.close() 
        print("Port balance fermé") 
        serial_conn = None 
        return True
"""