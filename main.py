# move.move by xibsy
import asyncio
import logging
import sys

from PyQt6.QtWidgets import QApplication

from qt import MainWindow
import bot

app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
try:
    asyncio.run(bot.main())
except KeyboardInterrupt:
    print("\nОстановлен пользователем")
except Exception as exception:
    logging.error(f"Непредвидинная ошибка: {exception}")

sys.exit(app.exec())