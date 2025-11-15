import sqlite3
from constants import DATABASE, RESERVATIONS_DATABASES, MIN_DATE


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
            stars INTEGER,
            permission INTEGER
            )
            ''')

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Permissions (
                    id INTEGER PRIMARY KEY,
                    permission TEXT NOT NULL
                    )
                    ''')

            for table in range(1, 7):
                cursor.execute(f'''
                                CREATE TABLE IF NOT EXISTS {RESERVATIONS_DATABASES[table]} (
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

            cursor.execute(f'INSERT INTO Users (username, chat_id, stars, permission) VALUES '
                           f'{(username, chat_id, 0, permission)}')

            connection.commit()

    def add_stars(self, added_stars: int, chat_id: int) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute(f'SELECT stars FROM Users WHERE chat_id = {chat_id}')
            stars_balance = cursor.fetchall()[0]

            cursor.execute(
                f'UPDATE Users SET stars = {stars_balance[0] + added_stars} WHERE chat_id = {chat_id}')

            connection.commit()

    def set_stars(self, set_stars: int, chat_id: int) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute(
                f'UPDATE Users SET stars = {set_stars} WHERE chat_id = {chat_id}')

            connection.commit()

    def get_stars_balance(self, chat_id: int) -> int:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute(f'SELECT stars FROM Users WHERE chat_id = {chat_id}')
            stars_balance = cursor.fetchall()[0]
            return stars_balance[0]


    def get_chat_id(self, username: str) -> int:

        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute(f'SELECT chat_id FROM Users WHERE username = ?', (username, ))

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

    def update_reservations(self) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            for table in range(1, 7):
                cursor.execute(f'DELETE FROM {RESERVATIONS_DATABASES[table]} '
                               f'WHERE date > {MIN_DATE - 1}')

            connection.commit()

    def append_reservation(self, table: int, username: str, date: str, time: str) -> None:
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute(
                f'INSERT INTO {RESERVATIONS_DATABASES[table]} (username, date, time) VALUES {(username, date, time)}')

            connection.commit()

    def get_reservations(self, table: int, date: str) -> list[str]:
        data = list()
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            cursor.execute(f'SELECT username, date, time FROM {RESERVATIONS_DATABASES[table]} WHERE date = {date}')

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
