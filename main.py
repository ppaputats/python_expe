# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

import sys 
from PyQt6.QtWidgets import QApplication 
from Software.UI.main_window import MainWindow

# ---------------------------------------------------------
# Définition main
# ---------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
