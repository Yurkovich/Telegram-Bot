import asyncio
from youtubesearchpython.__future__ import *
from pytube import YouTube
import re

async def check_duration(user_request: str):
    try:
        videosSearch = VideosSearch(
            user_request, limit=1, language='ru', region='RU')
        videosResult = await videosSearch.next()
        video_duration = videosResult["result"][0]["duration"]
        print(video_duration, type(video_duration))
        len_video_duration = len(video_duration)
        if len_video_duration <= 4:
            splited = video_duration.split(':')
            seconds = int(splited[0]) * 60 + int(splited[1])
            if seconds > 240:
                return False
            else:
                return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при проверке продолжительности видео: {e}")
        return False

async def get_url(user_request: str):
    try:
        videosSearch = VideosSearch(
            user_request, limit=1, language='ru', region='RU')
        videosResult = await videosSearch.next()

        video_url = videosResult["result"][0]["id"]
        video_title = videosResult["result"][0]["title"]
        result_url = f'https://www.youtube.com/watch?v={video_url}'

        return result_url
    except Exception as e:
        print(f"Ошибка при получении URL видео: {e}")
        return None

async def video_downloader(video_url, max_retries=3, retry_interval=10):
    for i in range(max_retries):
        try:
            my_video = YouTube(video_url)
            stream = my_video.streams.get_by_resolution('720p')
            video_title = simplify_video_title(my_video.title)
            video_title = f"{video_title}.mp4"
            stream.download(output_path='./downloads/video', filename=video_title)
            return video_title
        except Exception as e:
            print(f"Ошибка при загрузке видео: {e}")
            if i < max_retries - 1:
                print(f"Повторная попытка через {retry_interval} секунд...")
                await asyncio.sleep(retry_interval)
            else:
                print("Превышено количество попыток. Загрузка видео не удалась.")
                return None


# Допустимые символы в названии видео
def simplify_video_title(video_title):
    return re.sub(r'[^\w\s]', '', video_title)
