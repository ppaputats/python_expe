# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtGui import QPixmap

import Software.Request.Request_expe as Request_expe

import os
import shutil
from datetime import datetime

import Hardware.Scale.scale as Scale
import Hardware.Scale.scale_manager as ScaleManager
import Hardware.Camera.camera as camera
import Hardware.Printer.printer as Printer
import Hardware.Printer.printer_manager as PrinterManager

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

ip_printer,port_printer=0,0
class PalettePage(QWidget):
    def __init__(self, id_operateur, go_home_callback):
        super().__init__()

        # Création des dossiers si absents
        os.makedirs("photo", exist_ok=True)
        os.makedirs("etiquette", exist_ok=True)

        self.id_operateur = id_operateur
        self.go_home = go_home_callback
        self.id_pal = None
        self.url_photo1 = None
        self.url_photo2 = None
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
        self.label_poids = QLabel("Poids : -- kg")
        


        self.btn_photo = QPushButton("Prendre photo")
        self.btn_photo.clicked.connect(self.photo_action)


        self.preview1 = QLabel("Photo 1")
        self.preview2 = QLabel("Photo 2")

        self.btn_poids = QPushButton("Prendre poids")
        self.btn_poids.clicked.connect(self.take_weight)

        self.btn_imprimer = QPushButton("Imprimer étiquette")
        self.btn_imprimer.clicked.connect(self.print_label)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.save_all)

        self.btn_menu = QPushButton("Menu principal")
        self.btn_menu.clicked.connect(self.go_home)
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
        preview_line = QHBoxLayout()
        preview_line.addWidget(self.preview1)
        preview_line.addWidget(self.preview2)
        layout.addWidget(self.btn_photo)
        layout.addLayout(preview_line)

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



    def validate_bl(self):
        id_bl = self.input_bl.text().strip()
        if not id_bl.isdigit():
            QMessageBox.warning(self, "Erreur", "BL invalide")
            return

        # Vérifier que le BL existe
        if not Request_expe.bl_exists(int(id_bl)):
            QMessageBox.warning(self, "Erreur", "BL introuvable")
            return

        self.id_bl = int(id_bl)
        self.id_pal = Request_expe.get_next_id_pal_colis()

    def update_tare(self):
        type_pal = self.combo_type.currentText()
        tare = 0.5 if type_pal == "A" else 1.0
        self.label_tare.setText(f"Tare : {tare} kg")
        self.tare = tare
                
    def take_photo(self, num_photo):
        for i in range(1, 2):
            if camera.Connection_camera(i):
                file = camera.Photo_camera(i, self)
                if file:
                    if num_photo == 1:
                        self.preview1.setPixmap(QPixmap(file).scaled(300, 300))
                        self.temp_photo1 = file  # chemin temporaire
                    else:
                        self.preview2.setPixmap(QPixmap(file).scaled(300, 300))
                        self.temp_photo2 = file  # chemin temporaire
                camera.Close_camera(i)
            else:
                print("Erreur de connexion caméra", i)

    def save_photo(self):
        if hasattr(self, "temp_photo1"):
            self.url_photo1 = self.temp_photo1

        if hasattr(self, "temp_photo2"):
            self.url_photo2 = self.temp_photo2

    def take_weight(self): 
        print("Take_weight")
        self.tare = 0.5 
        # Lecture du poids via ScaleManager 
        poids_brut = ScaleManager.read_weight("palette") 
            
        if poids_brut is None: 
            QMessageBox.warning(self, "Erreur", "Impossible de lire le poids sur la balance palette.") 
            return 
        # Application de la tare 
        self.poids = poids_brut - self.tare 
          
        # Mise à jour de l'affichage 
        self.label_poids.setText(f"Poids avec tare : {self.poids:.2f} kg")


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


    
    def save_all(self):
        try:
            # Vérifier BL
            if not hasattr(self, "id_bl"):
                QMessageBox.warning(self, "Erreur", "Veuillez valider un BL avant d'enregistrer.")
                return

            # Vérifier poids
            if not hasattr(self, "poids"):
                QMessageBox.warning(self, "Erreur", "Veuillez mesurer le poids avant d'enregistrer.")
                return

            # Vérifier photos
            if not hasattr(self, "temp_photo1") or not hasattr(self, "temp_photo2"):
                QMessageBox.warning(self, "Erreur", "Veuillez prendre les deux photos.")
                return

            # Numéro de colis
            numero_colis = Request_expe.get_pal_data(self.id_pal)[1]

            if not self.url_etiquette:
                QMessageBox.warning(self, "Erreur", "Veuillez imprimer l'étiquette avant d'enregistrer.")
                return

            # Sauvegarde photos
            timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")

            filename1 = f"id_BL_{self.id_bl}__id_Pal_{self.id_pal}__{timestamp}__1.png"
            shutil.copy(self.temp_photo1, os.path.join("photo", filename1))
            self.url_photo1 = filename1

            filename2 = f"id_BL_{self.id_bl}__id_Pal_{self.id_pal}__{timestamp}__2.png"
            shutil.copy(self.temp_photo2, os.path.join("photo", filename2))
            self.url_photo2 = filename2

            # Enregistrement SQL
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

            Request_expe.insert_photo(self.id_pal, self.url_photo1, self.url_photo2)

            QMessageBox.information(self, "OK", "Palette enregistrée")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue :\n{e}")


    def photo_action(self):
        # Cas 1 : aucune photo → prendre photo 1
        if not hasattr(self, "temp_photo1"):
            self.take_photo(1)
            return

        # Cas 2 : photo 1 OK mais pas photo 2 → prendre photo 2
        if not hasattr(self, "temp_photo2"):
            self.take_photo(2)
            return

        # Cas 3 : les deux photos existent → proposer de les reprendre
        choix, ok = QInputDialog.getItem(
            self,
            "Reprendre photo",
            "Quelle photo voulez-vous reprendre ?",
            ["Photo 1", "Photo 2"],
            0,
            False
        )

        if ok:
            if choix == "Photo 1":
                self.take_photo(1)
            else:
                self.take_photo(2)
