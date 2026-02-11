# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from Software.UI.login_page import LoginPage
from Software.UI.main_page import MainPage
from Software.UI.colis_page import ColisPage
from Software.UI.palette_page import PalettePage
from Software.UI.admin_page import AdminPage

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interface expédition")
        self.resize(1200, 700)

        self.stacked = QStackedWidget()

        self.page_login = LoginPage()
        self.page_main = None

        self.stacked.addWidget(self.page_login)

        self.setCentralWidget(self.stacked)

        # Navigation
        self.page_login.login_success.connect(self.login)

        self.stacked.setCurrentWidget(self.page_login)

    def login(self, admin_mode, id_operateur):

        if admin_mode:
            self.page_admin = AdminPage()
            self.stacked.addWidget(self.page_admin)
            self.page_admin.btn_logout.clicked.connect(self.logout)
            self.stacked.setCurrentWidget(self.page_admin)
            return

        # Pages colis et palette
        self.page_colis = ColisPage(id_operateur, self.return_home)
        self.page_palette = PalettePage(id_operateur, self.return_home)

        self.stacked.insertWidget(2, self.page_colis)
        self.stacked.insertWidget(3, self.page_palette)

        self.page_main = MainPage(id_operateur)
        self.stacked.insertWidget(4, self.page_main)

        self.page_main.btn_colis.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_colis))
        self.page_main.btn_palette.clicked.connect(lambda: self.stacked.setCurrentWidget(self.page_palette))
        self.page_main.btn_logout.clicked.connect(self.logout)

        # Charger l’historique
        self.page_main.load_history()

        # Afficher la page principale
        self.stacked.setCurrentWidget(self.page_main)


    def logout(self):
        self.stacked.setCurrentWidget(self.page_login)

    def return_home(self):
        self.page_main.load_history()
        self.stacked.setCurrentWidget(self.page_main)
    
    def on_login(self,admin_mode, id_operateur):
        if admin_mode:
            self.setCentralWidget(AdminPage())
        else:
            self.setCentralWidget(MainPage(id_operateur))
