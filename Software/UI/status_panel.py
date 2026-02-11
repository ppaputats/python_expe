# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QColor, QPalette

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------


# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

class StatusLight(QLabel):
    def __init__(self, ok=False):
        super().__init__()
        self.setFixedSize(16, 16)
        self.setAutoFillBackground(True)
        self.set_status(ok)

    def set_status(self, ok):
        color = QColor("green") if ok else QColor("red")
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(pal)


class StatusPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.lights = {}

        def add(label, key):
            row = QHBoxLayout()
            light = StatusLight(False)
            row.addWidget(light)
            row.addWidget(QLabel(label))
            row.addStretch()
            layout.addLayout(row)
            self.lights[key] = light

        add("Caméra colis", "cam_colis")
        add("Caméra palette 1", "cam_p1")
        add("Caméra palette 2", "cam_p2")
        add("Balance colis", "scale_colis")
        add("Balance palette", "scale_palette")
        add("Imprimante", "printer")

        self.setLayout(layout)

    def update(self, statuses: dict):
        for key, ok in statuses.items():
            if key in self.lights:
                self.lights[key].set_status(ok)
