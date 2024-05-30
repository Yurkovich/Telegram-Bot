import logging
from fastapi import APIRouter, HTTPException, Request
import sqlite3

from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic
from schemas import QueryMusicSchema, User
from music import search_and_download_music

router = APIRouter()
security = HTTPBasic()

DATABASE_URL = r'C:\Education\Самоучеба\16.05.24\users.db'


@router.post('/download/')
async def download_music(request: Request, query_music: QueryMusicSchema):
    file_name = search_and_download_music(query=query_music.query)
    if file_name:
        return FileResponse(path=file_name, media_type="audio", filename=file_name)


@router.post("/api/login")
def login(user: User):
    logging.info(f"Received login request for username: {user.username}")

    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                   (user.username, user.password))
    db_user = cursor.fetchone()
    conn.close()

    logging.info(f"Database query result: {db_user}")

    if db_user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
