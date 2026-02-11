import json
import os

CONFIG_FILE = "Software/Config/config_devices.json"

DEFAULT_CONFIG = {
    "camera_colis": "",
    "camera_palette_1": "",
    "camera_palette_2": "",
    "balance_com": ""
}

class ConfigManager:
    """
    Gestionnaire de configuration pour les adresses hardware.
    Charge, sauvegarde et met à jour config_devices.json.
    """

    def __init__(self, path=CONFIG_FILE):
        self.path = path
        self.data = {}
        self.load()

    # ---------------------------------------------------------
    # Chargement du fichier JSON
    # ---------------------------------------------------------
    def load(self):
        if not os.path.exists(self.path):
            # Création automatique du fichier si absent
            self.data = DEFAULT_CONFIG.copy()
            self.save()
            return

        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)

            # Vérifie que toutes les clés existent
            changed = False
            for key, default_value in DEFAULT_CONFIG.items():
                if key not in self.data:
                    self.data[key] = default_value
                    changed = True

            if changed:
                self.save()

        except Exception:
            # Si le fichier est corrompu → recréation propre
            self.data = DEFAULT_CONFIG.copy()
            self.save()

    # ---------------------------------------------------------
    # Sauvegarde du fichier JSON
    # ---------------------------------------------------------
    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    # ---------------------------------------------------------
    # Lecture d'une clé
    # ---------------------------------------------------------
    def get(self, key):
        return self.data.get(key)

    # ---------------------------------------------------------
    # Modification d'une clé
    # ---------------------------------------------------------
    def set(self, key, value):
        self.data[key] = value
        self.save()

    # ---------------------------------------------------------
    # Récupérer toute la config
    # ---------------------------------------------------------
    def all(self):
        return self.data.copy()
