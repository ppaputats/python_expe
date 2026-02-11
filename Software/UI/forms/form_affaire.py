from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import Software.Request.Admin as Admin

class FormAffaire(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter une affaire")

        layout = QVBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID affaire")

        self.input_prod = QLineEdit()
        self.input_prod.setPlaceholderText("ID produit client")

        self.input_poids = QLineEdit()
        self.input_poids.setPlaceholderText("Poids affaire")

        btn = QPushButton("Ajouter")
        btn.clicked.connect(self.add)

        self.label_info = QLabel("")

        layout.addWidget(self.input_id)
        layout.addWidget(self.input_prod)
        layout.addWidget(self.input_poids)
        layout.addWidget(btn)
        layout.addWidget(self.label_info)

        self.setLayout(layout)

    def add(self):
        ok = Admin.insert_Affaire(
            self.input_id.text(),
            self.input_prod.text(),
            self.input_poids.text()
        )

        if ok:
            self.label_info.setText("Affaire ajoutée avec succès")
        else:
            self.label_info.setText("Erreur : affaire déjà existante")
