# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from Software.Config.config_manager import ConfigManager 
from Camera.camera_ids import Connection_camera, Photo_camera, Close_camera

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

config = ConfigManager()

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

def Capture_colis(path):
    ack_cam = True 
    id_cam=config.get("camera_colis")
    if Connection_camera(id_cam):
        Photo_camera(id_cam,path)
        Close_camera(id_cam)
    else :
        ack_cam=False
    return ack_cam

def Capture_palette(path1, path2):
    ack_cam = True 
    id_cam1=config.get("camera_palette_1")
    id_cam2=config.get("camera_palette_2")

    if Connection_camera(id_cam1):
        Photo_camera(id_cam1,path1)
        Close_camera(id_cam1)

    if Connection_camera(id_cam2):
        Photo_camera(id_cam2,path2)
        Close_camera(id_cam2)

    else:
        ack_cam=False

    return ack_cam

def Compress_ing(path):
    return True