from ids_peak import ids_peak

def main():
    # Initialisation de la librairie
    ids_peak.Library.Initialize()

    try:
        # Gestionnaire de périphériques
        device_manager = ids_peak.DeviceManager.Instance()
        device_manager.Update()

        # Vérifier qu'une caméra est trouvée
        if device_manager.Devices().empty():
            print("Aucune caméra IDS détectée")
        else:
            # Ouvrir la première caméra
            device = device_manager.Devices()[0].OpenDevice(ids_peak.DeviceAccessType_Control)
            print("Caméra ouverte :", device.DisplayName())

    finally:
        # Fermeture propre
        ids_peak.Library.Close()
        print("Librairie IDS Peak fermée")
