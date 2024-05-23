import sqlite3


def create_table():
    with sqlite3.connect(r'C:\Education\Самоучеба\16.05.24\users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_web (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        conn.commit()
        cursor.close()


def create_user(username: str, password: str):
    conn = sqlite3.connect(r'C:\Education\Самоучеба\16.05.24\users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users_web (username, password) VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    cursor.close()
    conn.close()


def authenticate_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(r'C:\Education\Самоучеба\16.05.24\users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username=? AND password=?
    ''', (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None
