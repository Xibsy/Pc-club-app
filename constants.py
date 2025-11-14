from datetime import  datetime
from datetime import timedelta

from aiogram.types import KeyboardButton

MIN_YEAR, MIN_MONTH, MIN_DATE = map(int, str(datetime.now().date()).split('-'))
MAX_YEAR, MAX_MONTH, MAX_DATE = map(int, str((datetime.now().date() + timedelta(days=7))).split('-'))

TOKEN = '8120034227:AAFTp099F7GbaOGSN-29FdoXi2CoI1q-u-o'
ADMIN_CHAT_ID = 2124114677

DATABASE = "resources/data.db"

RESERVATIONS_DATABASES = {
    1: 'ReservationsForTheFirstComputer', 2: 'ReservationsForASecondComputer',
    3: 'ReservationsForTheThirdComputer', 4: 'ReservationsForTheFourthComputer',
    5: 'ReservationsForTheFifthComputer', 6: 'ReservationsForTheSixthComputer',
}

START_BUTTONS = [[KeyboardButton(text="👤 Мой профиль")], [KeyboardButton(text="🖥 Забронировать компьютер")],
                 [KeyboardButton(text='💻 Написать разработчику')], [KeyboardButton(text='⚙ Админ панель')]]

COMPUTERS_RESERVATION_BUTTONS = ['Первый 💻', 'Второй 💻', 'Третий 💻',
                                 'Четвёртый 💻', 'Пятый 💻', 'Шестой 💻',
                                 'Назад']