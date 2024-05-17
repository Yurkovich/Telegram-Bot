import sqlite3


def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, telegram_id INT, telegram_name TEXT, username VARCHAR(30), password VARCHAR(50))''')
    conn.commit()
    conn.close()