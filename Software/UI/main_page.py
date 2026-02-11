# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit
)

from Software.UI.status_panel import StatusPanel
import Software.Request.Request_expe as Request_expe
import Hardware.Printer.printer as Printer

import os
import re

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition de la classe
# ---------------------------------------------------------

class MainPage(QWidget):
    def __init__(self,operateur_id):
        super().__init__()

        main = QHBoxLayout()
        self.operateur_id = operateur_id
        # Colonne gauche
        left = QVBoxLayout()
        self.status = StatusPanel()

        self.btn_colis = QPushButton("Prise de mesure colis")
        self.btn_palette = QPushButton("Prise de mesure palette")
        self.btn_logout = QPushButton("Déconnexion")

        left.addWidget(self.status)
        left.addSpacing(20)
        left.addWidget(self.btn_colis)
        left.addWidget(self.btn_palette)
        left.addStretch()
        left.addWidget(self.btn_logout)

        # Historique
        right = QVBoxLayout()
        right.addWidget(QLabel("Historique des 10 dernières mesures"))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un BL...")
        self.search_btn = QPushButton("Rechercher")
        self.search_btn.clicked.connect(self.search_bl)

        right.addWidget(self.search_input)
        right.addWidget(self.search_btn)


        self.table = QTableWidget() 
        self.table.setColumnCount(7) 
        self.table.setHorizontalHeaderLabels([ "id_BL", "id_pal_colis", "Client", "id_AR", "Opérateur", "Horodatage", "Action" ])
        right.addWidget(self.table)

        main.addLayout(left, 1)
        main.addLayout(right, 3)

        self.setLayout(main)

    # ---------------------------------------------------------
    # Définition des fonctions de la classe
    # ---------------------------------------------------------

    def load_history(self, id_bl_filter=None):

        """
        Fonction : Affiche l'historique des 10 dernières saisies et du bouton de réimpression
        Entrée : Vide
        Sortie : Vide (pointeur)
        """
            
        rows = Request_expe.read_last_palettes(10, id_bl_filter)

        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            id_bl, id_pal_colis, client, id_ar, operateur, horodatage = row

            self.table.setItem(i, 0, QTableWidgetItem(str(id_bl)))
            self.table.setItem(i, 1, QTableWidgetItem(str(id_pal_colis)))
            self.table.setItem(i, 2, QTableWidgetItem(str(client)))
            self.table.setItem(i, 3, QTableWidgetItem(str(id_ar)))
            self.table.setItem(i, 4, QTableWidgetItem(str(operateur)))
            self.table.setItem(i, 5, QTableWidgetItem(str(horodatage)))

            # Bouton réimpression
            btn = QPushButton("Réimprimer")
            btn.clicked.connect(lambda _, bl=id_bl: self.reprint_label(bl))


            self.table.setCellWidget(i, 6, btn)


    def find_pal_from_bl(self, id_bl):
        dossier = "etiquette"

        if not os.path.exists(dossier):
            return None

        pattern = re.compile(rf"id_BL_{id_bl}__id_Pal_(\d+)__")

        for filename in os.listdir(dossier):
            match = pattern.search(filename)
            if match:
                return int(match.group(1))

        return None

    def reprint_label(self, id_bl):

        id_pal_colis = self.find_pal_from_bl(id_bl)

        if id_pal_colis is None:
            print("Aucune étiquette trouvée pour ce BL")
            return

        # Récupérer les infos SQL
        poids, numero_colis = Request_expe.get_pal_data(id_pal_colis)
        client = Request_expe.get_client_data(id_bl)

        # Générer le ZPL
        zpl = Printer.ZPLCreator_printer(
            id_bl,
            id_pal_colis,
            self.operateur_id,
            client,
            poids,
            numero_colis
        )

        Printer.Connection_printer("IP", "PORT")
        Printer.ZPLSend_printer(True, zpl)
        Printer.Close_printer(True)
        
    def search_bl(self):

        """
        Fonction : Cherche les indos à partir d'un numéro de BL
        Entrée : BL
        Sortie : Vide (pointeur)
        """
        
        text = self.search_input.text().strip()
        if text.isdigit():
            self.load_history(int(text))
        else:
            self.load_history()
    
    

