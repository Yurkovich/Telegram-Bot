import sqlite3


def register_user(username, password, telegram_name, telegram_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, telegram_name, telegram_id) VALUES (?, ?, ?, ?)", (username, password, telegram_name, telegram_id))
    conn.commit()
    conn.close()
