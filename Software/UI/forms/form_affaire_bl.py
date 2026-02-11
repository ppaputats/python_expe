from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import Software.Request.Admin as Admin

class FormAffaireBL(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter une affaire à un BL")

        layout = QVBoxLayout()

        self.input_bl = QLineEdit()
        self.input_bl.setPlaceholderText("ID BL")

        self.input_affaire = QLineEdit()
        self.input_affaire.setPlaceholderText("ID affaire")

        self.input_quantite = QLineEdit()
        self.input_quantite.setPlaceholderText("Quantité")

        btn = QPushButton("Ajouter")
        btn.clicked.connect(self.add)

        self.label_info = QLabel("")

        layout.addWidget(self.input_bl)
        layout.addWidget(self.input_affaire)
        layout.addWidget(self.input_quantite)
        layout.addWidget(btn)
        layout.addWidget(self.label_info)

        self.setLayout(layout)

    def add(self):
        ok = Admin.insert_Affaire_BL(
            self.input_bl.text(),
            self.input_affaire.text(),
            self.input_quantite.text()
        )

        if ok:
            self.label_info.setText("Affaire ajoutée au BL avec succès")
        else:
            self.label_info.setText("Erreur : BL ou affaire inexistante")
