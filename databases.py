import sqlite3
# https://metanit.com/sql/mysql/2.5.php
try:
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    sqlite_create_table_query = '''CREATE TABLE auth (
                                Id INT PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                email text NOT NULL UNIQUE,
                                password VARCHAR(16) NOT NULL);'''

    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица SQLite создана")

    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")