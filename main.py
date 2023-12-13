from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
import sys


if __name__ == "__main__": 
    app = QApplication([])
    window = MainWindow()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec())