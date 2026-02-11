# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from Hardware.Printer.printer import ZPL_to_PNG, Close_printer, ZPLSend_printer, Connection_printer, ZPLCreator_printer
from Software.Config.config_manager import ConfigManager

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

config = ConfigManager()

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

def print_pal_colis(id_bl, id_pal, operateur, client, poids, numero_colis,path):
    
    ack_printer = True 
    id_printer=config.get("Printer")
    zpl=ZPLCreator_printer(id_bl, id_pal, operateur, client, poids, numero_colis)

    id_cam=config.get("camera_colis")
    if Connection_printer(id_printer,0):
        ZPLSend_printer(True,zpl)
        Close_printer(True)
        ZPL_to_PNG(zpl,path)
    else :
        ack_printer=False
    

    return ack_printer
