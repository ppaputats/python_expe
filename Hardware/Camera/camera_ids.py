# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

def Connection_camera(id_camera): 
    ack_cam = True 
    try: 
        # Exemple : tentative de connexion 
        # conn.cam(id_camera) 
        pass 
    except Exception as e: 
        print(f"Erreur de connexion à la caméra {id_camera} : {e}") 
        ack_cam = False 
    finally: 
        pass 
    return ack_cam

def Photo_camera(id_camera, path):
    ack_cam = True 
    try: 
        # Exemple : tentative de connexion 
        # conn.cam(id_camera) 
        pass 
    except Exception as e: 
        print(f"Erreur de prise de photo de la caméra {id_camera} : {e}") 
        ack_cam = False 
    finally: 
        pass 
    return ack_cam

def Close_camera(id_camera):
    ack_cam = True 
    try: 
        # Exemple : tentative de connexion 
        # conn.cam(id_camera) 
        pass 
    except Exception as e: 
        print(f"Erreur de déconnexion à la caméra {id_camera} : {e}") 
        ack_cam = False 
    finally: 
        pass 
    return ack_cam