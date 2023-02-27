import sqlite3


def auth_table_create():
    sqlite_connection = sqlite3.connect('../general_database.db')
    sqlite_create_table_query = '''CREATE TABLE Auth (
                                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Username VARCHAR(16) NOT NULL,
                                Password VARCHAR(16) NOT NULL);'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()


def general_info_table_create():
    sqlite_connection = sqlite3.connect('../general_database.db')
    sqlite_create_table_query = '''CREATE TABLE General_info (
                                UserId INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                                Username VARCHAR(16) NOT NULL,
                                Email TINYTEXT NOT NULL,
                                Phone INT,
                                Password VARCHAR(16) NOT NULL,
                                Avatar BLOB,
                                FOREIGN KEY (UserId) REFERENCES Auth (Id));'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()


def tokens_table_create():
    sqlite_connection = sqlite3.connect('../general_database.db')
    sqlite_create_table_query = '''CREATE TABLE Tokens (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                UserId INTEGER,
                                Token TINYTEXT UNIQUE,
                                FOREIGN KEY (UserId) REFERENCES Auth (Id));'''
    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()


auth_table_create()
general_info_table_create()
tokens_table_create()
