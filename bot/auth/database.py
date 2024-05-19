import sqlite3


def register_user(username, password, telegram_name, telegram_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, telegram_name, telegram_id) VALUES (?, ?, ?, ?)",
              (username, password, telegram_name, telegram_id))
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None


def save_query_to_database(user_id, username, query):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_queries (telegram_id, username, query) VALUES (?, ?, ?)",
              (user_id, username, query))
    conn.commit()
    conn.close()


def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, telegram_id INT, telegram_name TEXT, username VARCHAR(30), password VARCHAR(50))''')
    conn.commit()
    conn.close()


def create_queries_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_queries (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER,
            username TEXT,
            query TEXT,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()


def delete_account(id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()


def clear_queries(id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM user_queries WHERE id=?", (id,))
    conn.commit()
    conn.close()


