import random
import sqlite3
import string
import time


def generate_token():
    part1 = str(hash(time.time()))
    part1 = part1.replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e")
    part1 = part1.replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i")
    part2 = "".join(random.choices(string.digits + string.ascii_lowercase, k=15))
    token = "s.ch." + part1 + "." + part2
    return token


def check_token(id: int, token: str):
    connection = sqlite3.connect("general_database.db")
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT * FROM Tokens WHERE Token = (?) and UserId = (?);", (token, id))
    if data == "None":
        return 1
    else:
        return 0


def write_token(id: int, token: str):
    connection = sqlite3.connect("general_database.db")
    cursor = connection.cursor()
    cursor.execute('''INSERT into Tokens (UserId, Token) VALUES (?, ?)''',
                   (id, token)).fetchone()


def registry_new_acc(username: str, password: str, email: str, phone=None, avatar_image=None):
    connection = sqlite3.connect('general_database.db')
    cursor = connection.cursor()

    cursor.execute('''INSERT into Auth (Email, Password) VALUES (?, ?)''', (email, password)).fetchone()
    user_id = cursor.execute('''select max(Id) from Auth''').fetchone()
    user_id = user_id[0]
    token = generate_token()
    connection.commit()
    cursor.execute("""INSERT into General_info (UserId, Username, Email, Password) VALUES (?, ?, ?, ?)""",
                   (user_id, username, email, password)).fetchone()
    connection.commit()
    cursor.execute("INSERT into Tokens (UserId, Token) values (?, ?)", (user_id, token))
    connection.commit()

    cursor.close()
    connection.close()
    return token, user_id


def is_registry(email):
    connection = sqlite3.connect("general_database.db")
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT * FROM Auth WHERE Email = (?)", (email,)).fetchone()
    if data is None:
        return False
    else:
        return True


def data_correctly(nick, password):
    connection = sqlite3.connect("general_database.db")
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT * FROM Auth WHERE Email = (?) and Password = (?);", (nick, password))
    if is_registry(nick) == 0:
        return -1
    elif data == "None":
        return 1
    else:
        return 0


def get_id_by_email(email: str):
    connection = sqlite3.connect("general_database.db")
    cursor = connection.cursor()
    data = cursor.execute(
        "SELECT UserId FROM General_info WHERE Email = (?);", (email,)).fetchone()
    if data is None:
        return 1
    else:
        return data[0]



