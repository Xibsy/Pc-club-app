from PyQt6.QtCore import QTimer, QTime


class Timer:
    def __init__(self):
        self._timer = QTimer()
        self._time = QTime(2, 0, 0)

    def start_timer(self) -> str:
        self._timer.timeout.connect(self._)
        self._timer.start(7200)