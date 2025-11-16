from datetime import  datetime
from datetime import timedelta

from aiogram.types import KeyboardButton

from pandas import date_range


MIN_YEAR, MIN_MONTH, MIN_DATE = map(int, str(datetime.now().date()).split('-'))
MAX_YEAR, MAX_MONTH, MAX_DATE = map(int, str((datetime.now().date() + timedelta(days=6))).split('-'))

start_date = datetime(MIN_YEAR, MIN_MONTH, MIN_DATE)
end_date = datetime(MAX_YEAR, MAX_MONTH, MAX_DATE)
DATE_RANGE = date_range(
    min(start_date, end_date),
    max(start_date, end_date)
).strftime('%d').tolist()

TOKEN = '8120034227:AAFTp099F7GbaOGSN-29FdoXi2CoI1q-u-o'
ADMIN_CHAT_ID = 2124114677

DATABASE = "resources/data.db"

RESERVATIONS_DATABASES = {
    1: 'ReservationsForTheFirstComputer', 2: 'ReservationsForASecondComputer',
    3: 'ReservationsForTheThirdComputer', 4: 'ReservationsForTheFourthComputer',
    5: 'ReservationsForTheFifthComputer', 6: 'ReservationsForTheSixthComputer',
}

COMPUTER_INDEX = {'first_computer_button': 1, 'second_computer_button': 2, 'third_computer_button': 3,
                  'fourth_computer_button': 4, 'fifth_computer_button': 5, 'sixth_computer_button': 6}


START_BUTTONS = [[KeyboardButton(text="🖥 Забронировать компьютер")],
                 [KeyboardButton(text='💻 Написать разработчику')], [KeyboardButton(text='⚙ Админ панель')]]

COMPUTERS_RESERVATION_BUTTONS = ['Первый 💻', 'Второй 💻', 'Третий 💻',
                                 'Четвёртый 💻', 'Пятый 💻', 'Шестой 💻']

COMPUTERS_RESERVATION_ALIAS = {'Первый 💻': 1, 'Второй 💻': 2, 'Третий 💻': 3,
                                 'Четвёртый 💻': 4, 'Пятый 💻': 5, 'Шестой 💻': 6}
