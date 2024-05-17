from youtubesearchpython.__future__ import *
from pytube import YouTube
import re


async def get_url(user_request: str):
    videosSearch = VideosSearch(
        user_request, limit=1, language='ru', region='RU')
    videosResult = await videosSearch.next()

    video_url = videosResult["result"][0]["id"]
    video_title = videosResult["result"][0]["title"]
    result_url = f'https://www.youtube.com/watch?v={video_url}'

    return result_url


async def video_downloader(video_url):
    my_video = YouTube(video_url)
    stream = my_video.streams.get_highest_resolution()
    # Определяем имя файла, удаляем лишние символы
    video_title = simplify_video_title(my_video.title)
    # Добавляем расширение .mp4 к имени файла
    video_title = f"{video_title}.mp4"
    # Скачиваем видео с указанным именем файла
    stream.download(output_path='./downloads/video', filename=video_title)
    return video_title


def simplify_video_title(video_title):
    # Оставляем только буквы, цифры и пробелы в названии видео
    return re.sub(r'[^\w\s]', '', video_title)
