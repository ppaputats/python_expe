# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal

import Software.Request.Request_expe as Request_expe

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition des fonctions et classes
# ---------------------------------------------------------

class LoginPage(QWidget):

    login_success = pyqtSignal(bool, int)  
    # bool = admin_mode, int = id_operateur

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Connexion")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Nom d'utilisateur")

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Mot de passe")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)

        # --- Case à cocher mode admin ---
        self.checkbox_admin = QCheckBox("Mode administrateur")

        self.btn_login = QPushButton("Se connecter")
        self.btn_login.clicked.connect(self.try_login)

        layout.addWidget(self.label)
        layout.addWidget(self.error_label)
        layout.addWidget(self.input_user)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.checkbox_admin)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def try_login(self):

        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        admin_mode = self.checkbox_admin.isChecked()

        id_op, droit = Request_expe.check_login(username, password)

        if id_op is False:
            self.error_label.setText("Identifiants incorrects")
            return

        if admin_mode and droit != "admin":
            self.error_label.setText("Droits insuffisants pour le mode admin")
            return

        self.error_label.setText("")
        self.login_success.emit(admin_mode, id_op)
