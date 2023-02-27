import sqlite3


def regestry_new_acc(username: str, password: str, email: str, avatar_image=None):
    sqlite_connection = sqlite3.connect('general_database.db')
    sqlite_create_table_query = ''' select max(Id) from Auth '''
    cursor = sqlite_connection.cursor()
    user_id = cursor.execute(sqlite_create_table_query).fetchone()
    sqlite_connection.commit()
    user_id = user_id[0]

    cursor.close()
    sqlite_connection.close()


regestry_new_acc("test", "0000", "netu@mail.ru")
