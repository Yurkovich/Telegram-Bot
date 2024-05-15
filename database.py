import sqlite3

# Функция для создания соединения с базой данных
def create_connection():
    return sqlite3.connect('bot_database.db')

# Создание таблицы для запросов пользователей
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_queries (
                      id INTEGER PRIMARY KEY,
                      query TEXT
                      )''')
    conn.commit()
    conn.close()

# Добавление запроса пользователя в базу данных
def add_query(query):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_queries (query) VALUES (?)", (query,))
    conn.commit()
    conn.close()

# Получение всех запросов пользователя из базы данных
def get_all_queries():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_queries")
    rows = cursor.fetchall()
    conn.close()
    return rows

create_table()
