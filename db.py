import sqlite3
import random


class DataBase:
    # Устанавливаем соединение с базой данных
    def __init__(self):
        self.connection_db = sqlite3.connect("data.db")
        self.db = self.connection_db.cursor()
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            secret_key TEXT NOT NULL,
            balance INTEGER NOT NULL
            )
            """
        )

        # date поле будет в формате YY-MM-DD HH-MM-SS
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            from_user INTEGER,
            get_user INTEGER,
            many INTEGER NOT NULL,
            date DATETIME NOT NULL,
            FOREIGN KEY (from_user) REFERENCES users(id),
            FOREIGN KEY (get_user) REFERENCES users(id)
            )
            """
        )

    def generate_secret_key(self):
        key = ""
        for i in range(8):
            key += random.choice("1234567890")
        return key

    # Создаем таблицу Users

    def create_users_db(self, username, balance=0):
        """Функция для создания нового пользователя в бд(users)
        Args:
            username: имя пользователя
            balance: изначальный баланс пользователя, по умолчанию 0
        """
        try:
            self.db.execute(
                f"""
                    INSERT INTO users (username, secret_key, balance)
                    VALUES (?, ?, ?)
                    """,
                (username, self.generate_secret_key(), balance),
            )
            print(f"[+] Пользователь {username}, balance = {balance} успешно создан!")
        except Exception as e:
            print(
                "[-] Проверьте передоваемые значения или имя бд куда будут добавлены значения\nError:",
                e,
            )

    def create_transactions_db(self, from_user, get_user, many):
        """Функция для создания новых транзакций в бд(transactions)
        Args:
            from_user: кто отправил деньги(ОБЯЗАТЕЛЬНО УКАЗЫВАТЬ ID ПОЛЬЗОВАТЕЛЯ)
            get_user: кому отправил(ОБЯЗАТЕЛЬНО УКАЗЫВАТЬ ID ПОЛЬЗОВАТЕЛЯ)
            many: сколько отправил
        """
        try:
            self.db.execute(
                f"""
                    INSERT INTO transactions (from_user, get_user, many, date)
                    VALUES (?, ?, ?, datetime())
                    """,
                (
                    from_user,
                    get_user,
                    many,
                ),
            )
            print(
                f"[+] Транзакция успешно создана: {from_user} => {get_user} отправлено {many}, время:"
            )
        except Exception as e:
            print(
                "[-] Проверьте передоваемые значения или имя бд куда будут добавлены значения\nError:",
                e,
            )

    def update_data_db(self, database, id, name_data, data):
        """Функция для обоновления данных в бд по id
        Args:
            database: имя обновляемой бд
            id: идентификатор в таблице
            name_data: какое поле будем обновлять(поля описаны при создании таблиц в начале кода)
            data: сами данные которые подставлять вместо старых значений
        """
        try:
            self.db.execute(
                f"UPDATE {database} SET {name_data} = ?  WHERE id = ?", (data, id)
            )
            print(
                f"[+] Из таблицы {database}: Данные {id}, {name_data} = {data} успешно обновлены!"
            )
        except Exception as e:
            print(
                "[-] Проверьте передоваемые значения или имя обновляемой бд\nError:", e
            )

    def delete_db(self, database, id):
        """Функция для удаления строчки по ID
        Args:
            database: имя бд в которой будет удаление
            id: идентификатор в таблице для удаления
        """
        try:
            self.db.execute(f"DELETE FROM {database} WHERE id = ?", (id,))
            print(f"[+] Из бд {database}, строка {id} успешно удалена!")
        except Exception as e:
            print(
                "[-] Проверьте правильно ли указан удаляемый id или имя бд откуда удаляется\nError:",
                e,
            )

    # Получаем все данные из бд
    def get_all_db(self, database):
        """Функция для получения ВСЕХ значений из БД
        Args:
            database: имя бд из которой будут получены все строчки
        """
        try:
            return self.db.execute(f"SELECT * FROM {database}").fetchall()
        except Exception as e:
            print("[-] Правильно ли указано имя бд?\nError:", e)

    # Получает данные из таблицы, удовлетворяющие условию
    def get_condition_db(self, database, condition):
        """Функция для получения данных из бд ПО ОПРЕДЕЛЁННОМУ УСЛОВИЮ
        Args:
            database: бд в котрой будем брать данные
            condition: само условие(ДОЛЖЕН БЫТЬ СИНТАКСИС SQLite), например (balance > 1000)
        """
        try:
            return self.db.execute(
                f"SELECT * FROM {database} WHERE {condition} "
            ).fetchall()
        except Exception as e:
            print(
                "[-] Проверьте чтобы передоваемое условие было правильным или правильно указано имя бд",
                e,
            )

    # Сохраняем изменения и закрываем соединение
    def __del__(self):
        self.connection_db.commit()
        self.connection_db.close()


if __name__ == "__main__":
    db = DataBase()
    print(db.get_all_db("users"))
