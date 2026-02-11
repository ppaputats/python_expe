from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt

from Software.Config.config_manager import ConfigManager
from Hardware.device_scanner import scan_all_devices 

from Software.UI.forms.form_client import FormClient
from Software.UI.forms.form_bl import FormBL
from Software.UI.forms.form_affaire import FormAffaire
from Software.UI.forms.form_affaire_bl import FormAffaireBL
from Software.UI.forms.form_operateur import FormOperateur


class AdminPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ---------------------------------------------------------
        # TITRE
        # ---------------------------------------------------------
        title = QLabel("Menu Administrateur")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # ---------------------------------------------------------
        # BOUTONS FORMULAIRES
        # ---------------------------------------------------------
        btn_op = QPushButton("Ajouter un opérateur")
        btn_client = QPushButton("Ajouter un client")
        btn_bl = QPushButton("Ajouter un BL")
        btn_affaire = QPushButton("Ajouter une affaire")
        btn_affaire_bl = QPushButton("Ajouter une affaire à un BL")

        btn_op.clicked.connect(self.open_insert_operateur)
        btn_client.clicked.connect(self.open_insert_client)
        btn_bl.clicked.connect(self.open_insert_bl)
        btn_affaire.clicked.connect(self.open_insert_affaire)
        btn_affaire_bl.clicked.connect(self.open_insert_affaire_bl)

        layout.addWidget(btn_op)
        layout.addWidget(btn_client)
        layout.addWidget(btn_bl)
        layout.addWidget(btn_affaire)
        layout.addWidget(btn_affaire_bl)

        # ---------------------------------------------------------
        # BOUTON DECONNEXION
        # ---------------------------------------------------------
        self.btn_logout = QPushButton("Se déconnecter")
        layout.addWidget(self.btn_logout)

        # ---------------------------------------------------------
        # CONFIGURATION HARDWARE
        # ---------------------------------------------------------
        layout.addWidget(QLabel("\nConfiguration Hardware"))
        layout.addWidget(QLabel("----------------------------------"))

        self.config = ConfigManager()

        # Caméra colis
        layout.addWidget(QLabel("Caméra colis"))
        self.input_cam_colis = QLineEdit(self.config.get("camera_colis"))
        layout.addWidget(self.input_cam_colis)

        # Caméra palette 1
        layout.addWidget(QLabel("Caméra palette 1"))
        self.input_cam_pal1 = QLineEdit(self.config.get("camera_palette_1"))
        layout.addWidget(self.input_cam_pal1)

        # Caméra palette 2
        layout.addWidget(QLabel("Caméra palette 2"))
        self.input_cam_pal2 = QLineEdit(self.config.get("camera_palette_2"))
        layout.addWidget(self.input_cam_pal2)

        # Balance colis
        layout.addWidget(QLabel("Balance colis (COM)"))
        self.input_balance_colis = QLineEdit(self.config.get("balance_colis"))
        layout.addWidget(self.input_balance_colis)

        # Balance palette
        layout.addWidget(QLabel("Balance palette (COM)"))
        self.input_balance_palette = QLineEdit(self.config.get("balance_palette"))
        layout.addWidget(self.input_balance_palette)

        # ---------------------------------------------------------
        # BOUTON ENREGISTRER
        # ---------------------------------------------------------
        btn_save = QPushButton("Enregistrer la configuration")
        btn_save.clicked.connect(self.save)
        layout.addWidget(btn_save)

        # ---------------------------------------------------------
        # SCAN DES PERIPHERIQUES
        # ---------------------------------------------------------
        layout.addWidget(QLabel("\nScan des périphériques USB"))
        layout.addWidget(QLabel("----------------------------------"))

        btn_scan = QPushButton("Scanner les périphériques USB")
        btn_scan.clicked.connect(self.scan_devices)
        layout.addWidget(btn_scan)

        self.scan_output = QLabel("")
        self.scan_output.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.scan_output)

        self.setLayout(layout)

    # ---------------------------------------------------------
    # SAUVEGARDE
    # ---------------------------------------------------------
    def save(self):
        self.config.set("camera_colis", self.input_cam_colis.text())
        self.config.set("camera_palette_1", self.input_cam_pal1.text())
        self.config.set("camera_palette_2", self.input_cam_pal2.text())
        self.config.set("balance_colis", self.input_balance_colis.text())
        self.config.set("balance_palette", self.input_balance_palette.text())
        print("Configuration mise à jour.")

    # ---------------------------------------------------------
    # SCAN DES PERIPHERIQUES
    # ---------------------------------------------------------
    def scan_devices(self):
        devices = scan_all_devices()

        text = "=== CAMERAS IDS ===\n"
        for cam in devices["cameras"]:
            text += f"{cam['name']} | Serial : {cam['serial']}\n"

        text += "\n=== PORTS COM ===\n"
        for port in devices["com_ports"]:
            text += f"{port['device']} | {port['description']}\n"

        text += "\n=== USB BRUT ===\n"
        for usb in devices["usb"]:
            text += f"USB {usb['vendor_id']}:{usb['product_id']} Bus {usb['bus']} Addr {usb['address']}\n"

        self.scan_output.setText(text)

    # ---------------------------------------------------------
    # FORMULAIRES
    # ---------------------------------------------------------
    def open_insert_client(self):
        from Software.UI.forms.form_client import FormClient
        self.form = FormClient()
        self.form.show()

    def open_insert_operateur(self):
        from Software.UI.forms.form_operateur import FormOperateur
        self.form = FormOperateur()
        self.form.show()

    def open_insert_bl(self):
        from Software.UI.forms.form_bl import FormBL
        self.form = FormBL()
        self.form.show()

    def open_insert_affaire(self):
        from Software.UI.forms.form_affaire import FormAffaire
        self.form = FormAffaire()
        self.form.show()

    def open_insert_affaire_bl(self):
        from Software.UI.forms.form_affaire_bl import FormAffaireBL
        self.form = FormAffaireBL()
        self.form.show()

