import sqlite3
from resources.constants import DATABASE


class Database:
    def __init__(self, database: str = DATABASE) -> None:
        self._database = database

    def start_bd(self) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            permission INTEGER
            )
            ''')

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Permissions (
                    id INTEGER PRIMARY KEY,
                    permission TEXT NOT NULL
                    )
                    ''')

            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS ReservationsForTheFirstComputer (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL
                                )
                                ''')

            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS ReservationsForASecondComputer (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL
                                )
                                ''')

            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS ReservationsForTheThirdComputer (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL
                                )
                                ''')

            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS ReservationsForTheFourthComputer (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL
                                )
                                ''')

            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS ReservationsForTheFifthComputer (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL
                                )
                                ''')

            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS ReservationsForTheSixthComputer (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                date TEXT NOT NULL,
                                time TEXT NOT NULL
                                )
                                ''')

            connection.commit()

    def append_new_user(self, username: str, chat_id: int, permission: int) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT INTO Users (username, chat_id, permission) VALUES (?, ?, ?)',
                           (username, chat_id, permission))

            connection.commit()

    def get_chat_id(self, username: str) -> int:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT chat_id FROM Users WHERE username = ?', (username,))

            ids = cursor.fetchall()[0]

            return ids[0]

    @property
    def chats_ids(self) -> list[int]:
        exit_ids = []
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT chat_id FROM Users')

            ids = cursor.fetchall()

            for user_id in ids:
                exit_ids.append(user_id[0])
        return exit_ids
    
    def append_first_computer_reservation(self, username: str, date: str, time: str) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT INTO ReservationsForTheFirstComputer (username, date, time) VALUES (?, ?, ?)', 
                           (username, date, time))

            connection.commit()

    def append_second_computer_reservation(self, username: str, date: str, time: str) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT INTO ReservationsForASecondComputer (username, date, time) VALUES (?, ?, ?)',
                           (username, date, time))

            connection.commit()

    def append_third_computer_reservation(self, username: str, date: str, time: str) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT INTO ReservationsForTheThirdComputer (username, date, time) VALUES (?, ?, ?)',
                           (username, date, time))

            connection.commit()

    def append_fourth_computer_reservation(self, username: str, date: str, time: str) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT INTO ReservationsForTheFourthComputer (username, date, time) VALUES (?, ?, ?)',
                           (username, date, time))

            connection.commit()

    def append_fifth_computer_reservation(self, username: str, date: str, time: str) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT INTO ReservationsForTheFifthComputer (username, date, time) VALUES (?, ?, ?)',
                           (username, date, time))

            connection.commit()

    def append_sixth_computer_reservation(self, username: str, date: str, time: str) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('INSERT INTO ReservationsForTheSixthComputer (username, date, time) VALUES (?, ?, ?)',
                           (username, date, time))

            connection.commit()

    def get_reservations(self,table: str, date: str) -> list[str]:
        data = list()
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT username, date, time FROM ReservationsForTheFirstComputer WHERE date = ?', (date,))

            reservations = cursor.fetchall()

            for reservation in reservations:
                data.append(f'{reservation[0]}, {reservation[2]}')

        return data


class IsNewUser:
    def __init__(self, id: int):
        self._id = id
        self._is_new_id = True

    @property
    def check(self) -> bool:
        exit_ids = []
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT chat_id FROM Users')

            ids = cursor.fetchall()

            for user_id in ids:
                exit_ids.append(user_id[0])

        if self._id in exit_ids:
            self._is_new_id = False

        return self._is_new_id
