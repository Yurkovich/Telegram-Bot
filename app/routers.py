from fastapi import APIRouter, HTTPException
import sqlite3
from schemas import UserCreate
from music import search_and_download_music

router = APIRouter()

DATABASE_URL = r'C:\Education\Самоучеба\16.05.24\users.db'


def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()


@router.post("/register/")
def create_user(user: UserCreate):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, telegram_id, telegram_name) VALUES (?, ?, ?, ?)",
            # Устанавливаем значения None для полей telegram_id и telegram_name
            (user.username, user.password, None, None)
        )
        conn.commit()
        return {"username": user.username}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким именем уже зарегистрирован!")
    finally:
        conn.close()


@router.get("/download/")
async def download_music(query: str):
    try:
        result_file = search_and_download_music(query)
        return {"message": "Music downloaded successfully", "file_path": result_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


