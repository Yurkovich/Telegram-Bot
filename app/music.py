from pytube import Search, YouTube
import os
from fastapi import HTTPException
from fastapi.responses import FileResponse


def check_and_send_file(file_path: str):
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=os.path.basename(file_path))
    else:
        raise HTTPException(status_code=404, detail="File not found")


def search_and_download_music(query: str) -> str:
    result_search = Search(query)
    if len(result_search.results) > 0:
        url = f'https://www.youtube.com/watch?v={result_search.results[0].video_id}'
        yt = YouTube(url)
        output_path = r'C:\Education\Самоучеба\16.05.24\downloads'
        try:
            os.makedirs(output_path, exist_ok=True)
        except OSError as e:
            print(f"Ошибка создания директории: {e}")
            return None

        video = yt.streams.filter(only_audio=True).first()
        base_filename = video.default_filename
        mp3_filename = os.path.join(output_path, os.path.splitext(base_filename)[0] + '.mp3')
        
        if os.path.exists(mp3_filename):
            print("Файл уже существует")
            return mp3_filename

        downloaded_file = video.download(output_path=output_path)
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + '.mp3'
        if ext != '.mp3':
            os.rename(downloaded_file, new_file)
        return new_file
    else:
        print("Результаты поиска не найдены")
        return None
