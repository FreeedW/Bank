import sqlite3
import random

# Устанавливаем соединение с базой данных
connection_user = sqlite3.connect("data.db")
db = connection_user.cursor()


def generate_secret_key():
    key = ""
    for i in range(8):
        key += random.choice("1234567890")
    return key


# Создаем таблицу Users
db.execute(
    """
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
secret_key TEXT NOT NULL,
balance INTEGER NOT NULL
)
"""
)


db.execute(
    """
CREATE TABLE IF NOT EXISTS trans (
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


def create_user(username, balance):
    db.execute(
        """
        INSERT INTO Users (username, secret_key, balance)
        VALUES (?, ?, ?)
        """,
        (username, generate_secret_key(), balance),
    )
    print(f"[+] Пользователь {username}, balance = {balance} успешно создан!")


# Обнавляем данные по id юзера
# name_data - имя столбца в таблице
# data - значение
def update_user(id_username, name_data, data):
    db.execute(f"UPDATE Users SET {name_data} = ?  WHERE id = ?", (data, id_username))
    print(f"[+] Пользователь {id_username}, {name_data} = {data} успешно обновлен!")


def delete_user(id_delete_user):
    db.execute("DELETE FROM Users WHERE id = ?", (id_delete_user,))
    print(f"[+] Пользователь {delete_user} успешно удален!")


# Получаем все данные из бд
def get_all_user():
    db.execute(f"SELECT * FROM users")
    data = db.fetchall()
    return data


# Получает данные из таблицы, удовлетворяющие условию
def get_user_data(condition):
    db.execute(f"SELECT * FROM users WHERE {condition} ")
    data = db.fetchall()
    return data


create_user("test", 1002)
# update_user(2, "balance", 2000)
# delete_user(2)
# delete_user(1)
print(get_user_data("balance > 1000"))

# Сохраняем изменения и закрываем соединение
connection_user.commit()
connection_user.close()
