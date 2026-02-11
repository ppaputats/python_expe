from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import Software.Request.Admin as Admin

class FormOperateur(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter un opérateur")

        layout = QVBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID opérateur")

        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nom opérateur")

        self.input_droit = QLineEdit()
        self.input_droit.setPlaceholderText("Droit (admin / user)")

        self.input_mdp = QLineEdit()
        self.input_mdp.setPlaceholderText("Mot de passe")

        btn = QPushButton("Ajouter")
        btn.clicked.connect(self.add)

        self.label_info = QLabel("")

        layout.addWidget(self.input_id)
        layout.addWidget(self.input_nom)
        layout.addWidget(self.input_droit)
        layout.addWidget(self.input_mdp)
        layout.addWidget(btn)
        layout.addWidget(self.label_info)

        self.setLayout(layout)

    def add(self):
        ok = Admin.insert_operateur(
            self.input_id.text(),
            self.input_nom.text(),
            self.input_droit.text(),
            self.input_mdp.text()
        )

        if ok:
            self.label_info.setText("Opérateur ajouté avec succès")
        else:
            self.label_info.setText("Erreur : opérateur déjà existant")
