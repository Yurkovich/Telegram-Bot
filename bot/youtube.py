from youtubesearchpython.__future__ import *
from pytube import YouTube
import re

# Проверка для видео. Длительность не более 240 секунд
async def check_duration(user_request: str):
    videosSearch = VideosSearch(
        user_request, limit=1, language='ru', region='RU')
    videosResult = await videosSearch.next()
    video_duration = videosResult["result"][0]["duration"]

    splited = video_duration.split(':')
    seconds = int(splited[0]) * 60 + int(splited[1])
    if seconds > 240:
        return False
    else:
        return True

# Получение ссылки на видео
async def get_url(user_request: str):
    videosSearch = VideosSearch(
        user_request, limit=1, language='ru', region='RU')
    videosResult = await videosSearch.next()

    video_url = videosResult["result"][0]["id"]
    video_title = videosResult["result"][0]["title"]
    result_url = f'https://www.youtube.com/watch?v={video_url}'

    return result_url

# Загрузка видео с ютуба, удаление лишних символов и преобразование в .mp4
async def video_downloader(video_url):
    my_video = YouTube(video_url)
    stream = my_video.streams.get_by_resolution('720p')
    video_title = simplify_video_title(my_video.title)
    video_title = f"{video_title}.mp4"
    stream.download(output_path='./downloads/video', filename=video_title)
    return video_title

# Допустимые символы в названии видео
def simplify_video_title(video_title):
    return re.sub(r'[^\w\s]', '', video_title)
