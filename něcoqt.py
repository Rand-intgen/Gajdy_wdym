import sys
from PySide6 import QtWidgets, QtCore


class btnColorSwatch(QtWidgets.QPushButton):
    def __init__(self, color_hex, target_widget, parent=None):
        super().__init__(parent)
        self.color_hex = color_hex
        self.target_widget = target_widget  # ← widget, kterému budeme měnit barvu
        
        self.setFixedSize(24, 24)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        
        self.setStyleSheet(f"""
            background-color: {color_hex}; 
            border: 1px solid #ddd; 
            border-radius: 12px;
        """)
        
        self.clicked.connect(self.change_background)

    def change_background(self):
        if self.target_widget:
            # Změníme barvu pozadí
            self.target_widget.setStyleSheet(f"""
                background-color: {self.color_hex};
            """)
            print(f"Barva pozadí změněna na: {self.color_hex}")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Aplikace QT - Změna barvy pozadí")
        self.resize(500, 500)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        label = QtWidgets.QLabel("Klikni na barvu")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; margin: 20px;")
        
        main_layout.addWidget(label)

        # Předáváme central_widget jako cíl pro změnu barvy
        red_swatch = btnColorSwatch("#ff0000", central_widget)
        main_layout.addWidget(red_swatch, alignment=QtCore.Qt.AlignCenter)

        # Přidám ještě pár dalších barev pro lepší testování
        colors = ["#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff", "#ffa500"]
        for color in colors:
            swatch = btnColorSwatch(color, central_widget)
            main_layout.addWidget(swatch, alignment=QtCore.Qt.AlignCenter)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())