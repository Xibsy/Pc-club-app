#move.move но дипсик сола

import asyncio
import logging
import sys
import os

os.environ["QT_QPA_PLATFORM"] = "windows"  # или "xcb" на Linux

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from qt import MainWindow
import bot


class ApplicationManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.bot_task = None

    async def run_bot(self):
        try:
            await bot.main()
        except Exception as e:
            logging.error(f"Ошибка в боте: {e}")
            return 1
        return 0

    def run(self):
        try:
            self.window.show()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            self.bot_task = loop.create_task(self.run_bot())

            timer = QTimer()
            timer.timeout.connect(lambda: loop.run_until_complete(asyncio.sleep(0)))
            timer.start(100)

            return self.app.exec()

        except Exception as e:
            logging.error(f"Критическая ошибка: {e}")
            return 1
        finally:
            if self.bot_task and not self.bot_task.done():
                self.bot_task.cancel()
            if loop and not loop.is_closed():
                loop.close()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    app_manager = ApplicationManager()
    return app_manager.run()


if __name__ == "__main__":
    sys.exit(main())