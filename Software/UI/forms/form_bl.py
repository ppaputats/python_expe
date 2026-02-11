from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import Software.Request.Admin as Admin

class FormBL(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter un BL")

        layout = QVBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID BL")

        self.input_client = QLineEdit()
        self.input_client.setPlaceholderText("ID client")

        self.input_nbr = QLineEdit()
        self.input_nbr.setPlaceholderText("Nombre palettes/colis théorique")

        self.input_brut = QLineEdit()
        self.input_brut.setPlaceholderText("Poids théorique brut")

        self.input_net = QLineEdit()
        self.input_net.setPlaceholderText("Poids théorique net")

        self.input_poids = QLineEdit()
        self.input_poids.setPlaceholderText("Poids réel")

        btn = QPushButton("Ajouter")
        btn.clicked.connect(self.add)

        self.label_info = QLabel("")

        layout.addWidget(self.input_id)
        layout.addWidget(self.input_client)
        layout.addWidget(self.input_nbr)
        layout.addWidget(self.input_brut)
        layout.addWidget(self.input_net)
        layout.addWidget(self.input_poids)
        layout.addWidget(btn)
        layout.addWidget(self.label_info)

        self.setLayout(layout)

    def add(self):
        ok = Admin.insert_BL(
            self.input_id.text(),
            self.input_client.text(),
            self.input_nbr.text(),
            self.input_brut.text(),
            self.input_net.text(),
            self.input_poids.text()
        )

        if ok:
            self.label_info.setText("BL ajouté avec succès")
        else:
            self.label_info.setText("Erreur : BL déjà existant")
