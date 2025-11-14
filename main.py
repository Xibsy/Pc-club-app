import sys
from PyQt6.QtWidgets import QApplication
from qt import MainWindow


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec())