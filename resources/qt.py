import sys
from constants import MIN_YEAR, MAX_YEAR, MIN_MONTH, MAX_MONTH, MIN_DATE, MAX_DATE

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog, QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt6.QtCore import QDate
from qdarktheme import load_stylesheet

from resources.bot import database
from resources.sql import Database


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('ui.ui', self)

        self.setStyleSheet(load_stylesheet())

        self.reservations_calendar.setMinimumDate(QDate(MIN_YEAR, MIN_MONTH, MIN_DATE))
        self.reservations_calendar.setMaximumDate(QDate(MAX_YEAR, MAX_MONTH, MAX_DATE))

        # Set today's date as selected
        self.reservations_calendar.setSelectedDate(QDate.currentDate())

        # Connect signal for date selection
        self.reservations_calendar.selectionChanged.connect(self.on_date_selected)

        self.first_computer_button.clicked.connect(self.on_first_computer_button_click)
        self.second_computer_button.clicked.connect(self.on_second_computer_button_click)
        self.third_computer_button.clicked.connect(self.on_third_computer_button_click)
        self.fourth_computer_button.clicked.connect(self.on_fourth_computer_button_click)
        self.fifth_computer_button.clicked.connect(self.on_fifth_computer_button_click)
        self.sixth_computer_button.clicked.connect(self.on_sixth_computer_button_click)

        self.back_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.start_session_button.clicked.connect(lambda: self._dialog.exec())
        self.add_reservation_button.clicked.connect(self.on_add_reservation_button_click)

        self.white_theme_button.triggered.connect(lambda: self.setStyleSheet(load_stylesheet('light')))
        self.black_theme_button.triggered.connect(lambda: self.setStyleSheet(load_stylesheet()))

        self._database = Database()
        self._database.start_bd()
        self._database.update_reservations()

        self._dialog = Start_session_dialog()
        self._selected_computer = int()

    def on_date_selected(self):
        selected_date = self.reservations_calendar.selectedDate()
        reservations = self._database.get_reservations(self._selected_computer ,selected_date.day())
        self.reservations_list.clear()
        self.reservations_list.addItems(reservations)

    def on_add_reservation_button_click(self) -> None:
        data, ok_pressed = QInputDialog.getText(self, "Введите параметры брони",
                                                "Формат ввода TG username, День, Время")
        username, data, time = data.split(', ')
        if ok_pressed:
            database.append_reservation(self._selected_computer, username, data, time)


    def on_first_computer_button_click(self) -> None:
        self.stackedWidget.setCurrentIndex(1)
        self._selected_computer = 1

    def on_second_computer_button_click(self) -> None:
        self.stackedWidget.setCurrentIndex(1)
        self._selected_computer = 2

    def on_third_computer_button_click(self) -> None:
        self.stackedWidget.setCurrentIndex(1)
        self._selected_computer = 3

    def on_fourth_computer_button_click(self) -> None:
        self.stackedWidget.setCurrentIndex(1)
        self._selected_computer = 4

    def on_fifth_computer_button_click(self) -> None:
        self.stackedWidget.setCurrentIndex(1)
        self._selected_computer = 5

    def on_sixth_computer_button_click(self) -> None:
        self.stackedWidget.setCurrentIndex(1)
        self._selected_computer = 6

class Start_session_dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Запуск сеанса")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Запустить сессию?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())