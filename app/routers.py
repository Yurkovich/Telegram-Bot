from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from schemas import UserSchemaCreate

router = APIRouter()

DATABASE_URL = r'C:\Education\Самоучеба\16.05.24\users.db'

def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

@router.post("/users/")
def create_user(user: UserSchemaCreate):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users_web (username, password) VALUES (?, ?)",
            (user.username, user.password)  # Пароль пока сохраняем как есть, без хеширования
        )
        conn.commit()
        return {"username": user.username}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")
    finally:
        conn.close()