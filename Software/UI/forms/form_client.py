from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import Software.Request.Admin as Admin

class FormClient(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ajouter un client")

        layout = QVBoxLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID client")

        self.input_dep = QLineEdit()
        self.input_dep.setPlaceholderText("Département de livraison")

        self.input_adresse = QLineEdit()
        self.input_adresse.setPlaceholderText("Adresse de livraison")

        self.input_contact = QLineEdit()
        self.input_contact.setPlaceholderText("Contact")

        btn = QPushButton("Ajouter")
        btn.clicked.connect(self.add)

        self.label_info = QLabel("")

        layout.addWidget(self.input_id)
        layout.addWidget(self.input_dep)
        layout.addWidget(self.input_adresse)
        layout.addWidget(self.input_contact)
        layout.addWidget(btn)
        layout.addWidget(self.label_info)

        self.setLayout(layout)

    def add(self):
        ok = Admin.insert_client(
            self.input_id.text(),
            self.input_dep.text(),
            self.input_adresse.text(),
            self.input_contact.text()
        )

        if ok:
            self.label_info.setText("Client ajouté avec succès")
        else:
            self.label_info.setText("Erreur : client déjà existant")
