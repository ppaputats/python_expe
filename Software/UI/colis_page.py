# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtGui import QPixmap

import Software.Request.Request_expe as Request_expe
import Hardware.Scale.scale as Scale
import Hardware.Scale.scale_manager as ScaleManager
import Hardware.Camera.camera as camera
import Hardware.Printer.printer as Printer
import Hardware.Printer.printer_manager as PrinterManager

from datetime import datetime
import os
import shutil

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

ip_printer,port_printer=0,0

# ---------------------------------------------------------
# Définition des fonctions et classes
# ---------------------------------------------------------

class ColisPage(QWidget):
    def __init__(self, id_operateur, go_home_callback):
        super().__init__()

        # Création des dossiers si absents
        os.makedirs("photo", exist_ok=True)
        os.makedirs("etiquette", exist_ok=True)


        self.id_operateur = id_operateur
        self.go_home = go_home_callback
        self.id_pal = None
        self.url_photo1 = None
        self.url_etiquette = None

        # --- UI ---
        self.input_bl = QLineEdit()
        self.btn_valider_bl = QPushButton("Valider BL")
        self.btn_valider_bl.clicked.connect(self.validate_bl)

        self.combo_type = QComboBox()
        self.combo_type.addItems(["A", "B"])
        self.combo_type.currentTextChanged.connect(self.update_tare)

        self.label_tare = QLabel("Tare : 0.5 kg")
        self.tare = 0.5

        self.btn_photo = QPushButton("Prendre photo")
        self.btn_photo.clicked.connect(self.photo_action)

        self.preview = QLabel("Aucune photo")

        self.btn_poids = QPushButton("Prendre poids")
        self.btn_poids.clicked.connect(self.take_weight)

        self.label_poids = QLabel("Poids : -- kg")

        self.btn_imprimer = QPushButton("Imprimer étiquette")
        self.btn_imprimer.clicked.connect(self.print_label)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.save_all)

        self.btn_menu = QPushButton("Menu principal")
        self.btn_menu.clicked.connect(self.go_home)

        # --- Layout ---
        layout = QVBoxLayout()

        # Ligne BL
        bl_line = QHBoxLayout()
        bl_line.addWidget(QLabel("Numéro BL :"))
        bl_line.addWidget(self.input_bl)
        bl_line.addWidget(self.btn_valider_bl)
        layout.addLayout(bl_line)

        # Type palette
        type_line = QHBoxLayout()
        type_line.addWidget(QLabel("Type palette :"))
        type_line.addWidget(self.combo_type)
        type_line.addWidget(self.label_tare)
        layout.addLayout(type_line)

        # Photo
        layout.addWidget(self.btn_photo)
        layout.addWidget(self.preview)

        # Poids
        layout.addWidget(self.btn_poids)
        layout.addWidget(self.label_poids)

        # Impression
        layout.addWidget(self.btn_imprimer)

        # Enregistrement
        layout.addWidget(self.btn_save)

        # Menu principal
        layout.addWidget(self.btn_menu)

        self.setLayout(layout)

    # -----------------------------
    # LOGIQUE
    # -----------------------------

    def validate_bl(self):
        id_bl = self.input_bl.text().strip()
        if not id_bl.isdigit():
            QMessageBox.warning(self, "Erreur", "BL invalide")
            return

        if not Request_expe.bl_exists(int(id_bl)):
            QMessageBox.warning(self, "Erreur", "BL introuvable")
            return

        self.id_bl = int(id_bl)
        self.id_pal = Request_expe.get_next_id_pal_colis()

    def update_tare(self):
        type_pal = self.combo_type.currentText()
        self.tare = 0.5 if type_pal == "A" else 1.0
        self.label_tare.setText(f"Tare : {self.tare} kg")

    # -----------------------------
    # PHOTO
    # -----------------------------

    def take_photo(self):
        if camera.Connection_camera(0):
            file = camera.Photo_camera(0, self)
            if file:
                self.preview.setPixmap(QPixmap(file).scaled(300, 300))
                self.temp_photo = file  # chemin temporaire
            camera.Close_camera(0)

        else:
            print("Erreur de connexion caméra 0")

    def photo_action(self):
        if not hasattr(self, "temp_photo"):
            self.take_photo()
            return

        choix = QMessageBox.question(
            self,
            "Reprendre photo",
            "Voulez-vous reprendre la photo ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if choix == QMessageBox.StandardButton.Yes:
            self.take_photo()


    # -----------------------------
    # POIDS
    # -----------------------------

    def take_weight(self): 
        print("Take_weight")
        self.tare = 0.5 
        # Lecture du poids via ScaleManager 
        poids_brut = ScaleManager.read_weight("colis") 
            
        if poids_brut is None: 
            QMessageBox.warning(self, "Erreur", "Impossible de lire le poids sur la balance palette.") 
            return 
        # Application de la tare 
        self.poids = poids_brut - self.tare 
          
        # Mise à jour de l'affichage 
        self.label_poids.setText(f"Poids avec tare : {self.poids:.2f} kg")

    # -----------------------------
    # ÉTIQUETTE
    # -----------------------------

    def print_label(self):
        if not hasattr(self, "id_bl") or not hasattr(self, "id_pal"):
            QMessageBox.warning(self, "Erreur", "BL ou palette non défini.")
            return

        timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
        filename = f"id_BL_{self.id_bl}__id_Pal_{self.id_pal}__{timestamp}.png"
        dest = os.path.join("etiquette", filename)

        # Numéro de colis
        numero_colis = Request_expe.count_colis_for_bl(self.id_bl) + 1
        client = Request_expe.get_client_data(self.id_bl)

        # Génération ZPL
        if PrinterManager.print_pal_colis(
            self.id_bl,
            self.id_pal,
            self.id_operateur,
            client,
            getattr(self, "poids", 0),
            numero_colis,
            dest
        ):
            print("Etiquette imprimé")
        else : 
            print("Problème impression")


        self.url_etiquette = filename

        QMessageBox.information(self, "Étiquette", f"Étiquette générée :\n{filename}")

    # -----------------------------
    # ENREGISTREMENT
    # -----------------------------

    def save_all(self):
        try:
            if not hasattr(self, "id_bl"):
                QMessageBox.warning(self, "Erreur", "Veuillez valider un BL.")
                return

            if not hasattr(self, "poids"):
                QMessageBox.warning(self, "Erreur", "Veuillez mesurer le poids.")
                return

            if not hasattr(self, "temp_photo"):
                QMessageBox.warning(self, "Erreur", "Veuillez prendre une photo.")
                return


            if not self.url_etiquette:
                QMessageBox.warning(self, "Erreur", "Veuillez imprimer l'étiquette.")
                return
            
            # Numéro de colis
            numero_colis = Request_expe.get_pal_data(self.id_pal)[1]

    
            # --- Enregistrement réel de la photo ---
            timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")

            filename = f"id_BL_{self.id_bl}__id_Pal_{self.id_pal}__{timestamp}__0.png"
            shutil.copy(self.temp_photo, os.path.join("photo", filename))
            self.url_photo1 = filename



            Request_expe.insert_pal_colis(
                self.id_pal,
                self.id_bl,
                self.combo_type.currentText(),
                self.tare,
                self.poids,
                self.id_operateur,
                self.url_etiquette,
                numero_colis
            )

            Request_expe.insert_photo(self.id_pal, self.url_photo1, None)

            QMessageBox.information(self, "OK", "Colis enregistré")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue :\n{e}")
