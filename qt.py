import sys
from constants import MIN_YEAR, MAX_YEAR, MIN_MONTH, MAX_MONTH, MIN_DATE, MAX_DATE

from PyQt6.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt6.QtCore import QDate, QTimer
from qdarktheme import load_stylesheet

from start_session_dialog import StartSessionDialog
from ui import Ui_MainWindow

from sql import Database

from warns import Warns


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setStyleSheet(load_stylesheet())

        self.reservations_calendar.setMinimumDate(QDate(MIN_YEAR, MIN_MONTH, MIN_DATE))
        self.reservations_calendar.setMaximumDate(QDate(MAX_YEAR, MAX_MONTH, MAX_DATE))
        self.reservations_calendar.setSelectedDate(QDate.currentDate())

        self.block_session_button.setEnabled(False)

        self.first_computer_button.clicked.connect(self.on_first_computer_button_click)
        self.second_computer_button.clicked.connect(self.on_second_computer_button_click)
        self.third_computer_button.clicked.connect(self.on_third_computer_button_click)
        self.fourth_computer_button.clicked.connect(self.on_fourth_computer_button_click)
        self.fifth_computer_button.clicked.connect(self.on_fifth_computer_button_click)
        self.sixth_computer_button.clicked.connect(self.on_sixth_computer_button_click)

        self.reservations_calendar.selectionChanged.connect(self.on_date_selected)
        self.back_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.start_session_button.clicked.connect(self.on_start_session_button_click)
        self.add_reservation_button.clicked.connect(self.on_add_reservation_button_click)
        self.add_five_minutes_button.clicked.connect(self.on_add_five_minutes_button_click)
        self.remove_five_minutes_button.clicked.connect(self.on_remove_five_minutes_button_click)
        self.block_session_button.clicked.connect(self.on_block_session_button_click)
        self.remove_one_warning_button.clicked.connect(self.on_remove_one_warning_button_click)
        self.send_warning_button.clicked.connect(self.on_send_warning_clicked)

        self.white_theme_button.triggered.connect(lambda: self.setStyleSheet(load_stylesheet('light')))
        self.black_theme_button.triggered.connect(lambda: self.setStyleSheet(load_stylesheet()))

        self._database = Database()
        self._database.start_bd()
        self._database.update_reservations()

        self._dialog = StartSessionDialog()
        self._selected_computer = 1

        self._warns_system = Warns()

        self._computer_remaining_time = {i: 0 for i in range(1, 7)}
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_all_timers)
        self.update_timer.start(1000)

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
            self._database.append_reservation(self._selected_computer, username, data, time)

    def on_start_session_button_click(self) -> None:
        if self._dialog.exec():
            self.start_timer()

    def start_timer(self) -> None:
        self._computer_remaining_time[self._selected_computer] = 7200

    def update_all_timers(self) -> None:
        for selected_computer in range(1, 7):
            if self._computer_remaining_time[selected_computer] > 0:
               self._computer_remaining_time[selected_computer] -= 1

        self.update_current_display(self._selected_computer)

    def update_current_display(self, selected_computer: int) -> None:
        time_left = self._computer_remaining_time[selected_computer]
        if time_left > 0:
            hours = time_left // 3600
            minutes = (time_left % 3600) // 60
            seconds = time_left % 60
            self.label_2.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.label_2.setText("00:00:00")

    def on_add_five_minutes_button_click(self) -> None:
        self._computer_remaining_time[self._selected_computer] += 300
        self.update_current_display(self._selected_computer)

    def on_remove_five_minutes_button_click(self) -> None:
        self._computer_remaining_time[self._selected_computer] -= 300
        self.update_current_display(self._selected_computer)

    def on_block_session_button_click(self) -> None:
        self._warns_system.set_warns(self._selected_computer, 0)
        self.update_warns()
        self._computer_remaining_time[self._selected_computer] = 0
        self.update_current_display(self._selected_computer)

    def update_warns(self) -> None:
        count_warns = self._warns_system.get_warns_for_selected_computer(self._selected_computer)
        self.label_4.setText(f'{count_warns}')
        if count_warns >= 3:
            self.remove_one_warning_button.setEnabled(False)
            self.send_warning_button.setEnabled(False)
            self.block_session_button.setEnabled(True)
        else:
            self.remove_one_warning_button.setEnabled(True)
            self.send_warning_button.setEnabled(True)
            self.block_session_button.setEnabled(False)

    def on_remove_one_warning_button_click(self) -> None:
        self._warns_system.remove_warn(self._selected_computer)
        self.update_warns()

    def on_send_warning_clicked(self) -> None:
        self._warns_system.add_warn(self._selected_computer)
        self.update_warns()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())